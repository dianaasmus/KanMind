from rest_framework import serializers
from board_app.models import Board, Task, Comment
from django.contrib.auth.models import User


# class PrimaryKeyRelatedField(serializers.ModelSerializer):
#     class Meta:
#         model = Member
#         fields = "__all__"


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


class TasksListSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    reviewer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    comments = TaskCommentsListSerializer(many=True, write_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments",
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

        return super().create(validated_data)

    def get_comments_count(self, obj):
        return obj.comments.count()


class TaskSerializer(TasksListSerializer):
    comments = TaskCommentSingleSerializer(many=True, read_only=True)

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
            "comments",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class BoardSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True
    )
    tasks = TaskSerializer(many=True, read_only=True)
    owner_data = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(read_only=True)
    members_data = serializers.SerializerMethodField()

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
