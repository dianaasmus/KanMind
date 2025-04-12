from rest_framework import serializers
from board_app.models import Board, Task, Comment
from django.contrib.auth.models import User


class TaskCommentSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class BoardListSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True
    )
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "members",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        members = validated_data.pop("members", [])
        owner = User.objects.get(email=request.user.email)

        board = Board.objects.create(owner=owner, **validated_data)
        board.members.set(members)
        board.members.add(owner)

        return board

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(status="high").count()


class TaskCommentsListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]

    def get_author(self, obj):
        return obj.author.fullname


class BaseTaskSerializer(serializers.ModelSerializer):
    assignee = serializers.SerializerMethodField()
    reviewer = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_assignee(self, obj):
        if obj.assignee:
            return UserSerializer(obj.assignee).data
        return None

    def get_reviewer(self, obj):
        if obj.reviewer:
            return UserSerializer(obj.reviewer).data
        return None


class TasksListSerializer(BaseTaskSerializer):
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    board_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta(BaseTaskSerializer.Meta):
        fields = [
            "id",
            "board",
            "board_id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        assignee_id = request.data.get("assignee_id")
        reviewer_id = request.data.get("reviewer_id")

        if assignee_id:
            validated_data["assignee"] = User.objects.get(id=assignee_id)
        if reviewer_id:
            validated_data["reviewer"] = User.objects.get(id=reviewer_id)

        validated_data["creator"] = request.user

        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request = self.context.get("request")
        if request and request.method == "POST":
            representation.pop("board", None)
        else:
            representation.pop("board_id", None)

        return representation


class TaskSerializer(BaseTaskSerializer):

    class Meta(BaseTaskSerializer.Meta):
        fields = BaseTaskSerializer.Meta.fields

    def update(self, instance, validated_data):
        request = self.context.get("request")
        assignee_id = request.data.get("assignee_id")
        reviewer_id = request.data.get("reviewer_id")
        board = request.data.get("board")

        if board:
            raise serializers.ValidationError({"board": "Board can not be updated"})

        if assignee_id:
            try:
                assignee = User.objects.get(id=assignee_id)
                if assignee not in instance.board.members.all():
                    raise serializers.ValidationError(
                        {"assignee_id": "User is not a member of this board."}
                    )
                validated_data["assignee"] = assignee
            except User.DoesNotExist:
                raise serializers.ValidationError({"assignee_id": "User not found."})

        if reviewer_id:
            try:
                reviewer = User.objects.get(id=reviewer_id)
                if reviewer not in instance.board.members.all():
                    raise serializers.ValidationError(
                        {"reviewer_id": "User is not a member of this board."}
                    )
                validated_data["reviewer"] = reviewer
            except User.DoesNotExist:
                raise serializers.ValidationError({"reviewer_id": "User not found."})

        return super().update(instance, validated_data)

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.method in ["PATCH"]:
            fields.pop("comments", None)
            fields.pop("comments_count", None)
        return fields


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=225, write_only=True)
    first_name = serializers.CharField(max_length=50, write_only=True)
    last_name = serializers.CharField(max_length=50, write_only=True)
    fullname = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "fullname"]

    def get_fullname(self, obj):
        return obj.first_name + " " + obj.last_name


class BoardSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    members_data = serializers.SerializerMethodField(read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    owner_data = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_id",
            "owner_data",
            "members",
            "members_data",
            "tasks",
        ]

    def get_owner_data(self, obj):
        return UserSerializer(obj.owner).data

    def get_members_data(self, obj):
        return UserSerializer(obj.members.all(), many=True).data

    def to_representation(self, value):
        representation = super().to_representation(value)
        request = self.context.get("request")

        if request:
            if request.method == "PATCH":
                representation.pop("members", None)
                representation.pop("owner_id", None)
                representation.pop("tasks", None)
            else:
                representation.pop("owner_data", None)
                representation.pop("members_data", None)

        return representation
