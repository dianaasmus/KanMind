from rest_framework import serializers
from board_app.models import Board, Member, Task


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
    pass


class BoardDetailSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)
    tasks = TaskDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = "__all__"
