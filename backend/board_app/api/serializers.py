from rest_framework import serializers
from board_app.models import Board, Member, Task, Comment


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class BoardListSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(), many=True, write_only=True
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
        owner = request.user

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


class TaskListSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(), write_only=True
    )
    board_id = serializers.IntegerField(source="board.id", read_only=True)
    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    comments = serializers.CharField(write_only=True)

    class Meta:
        model = Task
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
            "comments",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        assignee_id = request.data.get("assignee_id")
        reviewer_id = request.data.get("reviewer_id")

        if assignee_id:
            validated_data["assignee"] = Member.objects.get(id=assignee_id)
        if reviewer_id:
            validated_data["reviewer"] = Member.objects.get(id=reviewer_id)

        return super().create(validated_data)


class TaskDetailSerializer(TaskListSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskUpdateSerializer(TaskListSerializer):
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
        ]


class BoardDetailSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    tasks = TaskDetailSerializer(many=True, read_only=True)
    owner_data = serializers.SerializerMethodField()
    members_data = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members_data", "members", "tasks"]

    def get_owner_data(self, obj):
        return MemberSerializer(obj.owner).data

    def get_members_data(self, obj):
        return MemberSerializer(obj.members.all(), many=True).data


class BoardUpdateSerializer(serializers.ModelSerializer):
    owner_data = serializers.SerializerMethodField(read_only=True)
    members_data = serializers.SerializerMethodField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(), many=True, required=False, write_only=True
    )

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members", "members_data"]

    def get_owner_data(self, obj):
        return MemberSerializer(obj.owner).data

    def get_members_data(self, obj):
        return MemberSerializer(obj.members.all(), many=True).data

    def update(self, instance, validated_data):
        if "title" in validated_data:
            instance.title = validated_data.get("title")

        if "members" in validated_data:
            members = validated_data.get("members")
            owner_in_members = any(member.id == instance.owner.id for member in members)
            if not owner_in_members:
                members.append(instance.owner)

            instance.members.set(members)

        instance.save()
        return instance


class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]

    def get_author(self, obj):
        return obj.author.fullname


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
