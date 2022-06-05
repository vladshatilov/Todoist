from django.db import transaction
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField

from core.models import Profile
from core.serializers import UserDetailSerializer
from goals.models import Board, BoardParticipant, Comment, Goal, GoalCategory


def category_validator(value: GoalCategory, user):
    if value.is_deleted:
        raise serializers.ValidationError("not allowed in deleted category")

    if value.user != user:
        raise serializers.ValidationError("not owner of category")
    return value


# GoalCategory
class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "board")


# Goal
class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = PrimaryKeyRelatedField(queryset=GoalCategory.objects.all())

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def create(self, validated_data):
        category_item = validated_data.pop('category')
        validated_category_item = category_validator(category_item, self.context["request"].user)
        goal = Goal.objects.create(category_id=validated_category_item.id, **validated_data)
        return goal


class GoalSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        # read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value):
        category_validator(value, self.context["request"].user)


# Goal Comment
class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    # goal = PrimaryKeyRelatedField(queryset=Goal.objects.all())

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "goal")


# Board Comment
class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.editable_choices
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=Profile.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def create(self, validated_data):
        # user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(user=self.context["request"].user, board=board, role=BoardParticipant.Role.owner)
        return board


class BoardSerializer(serializers.ModelSerializer):
    board_participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):
        owner = validated_data.pop("user")
        new_participants = validated_data.pop("participants")
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.board_participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if old_participant.role != new_by_id[old_participant.user_id]["role"]:
                        old_participant.role = new_by_id[old_participant.user_id]["role"]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
                for new_part in new_by_id.values():
                    BoardParticipant.objects.create(
                        board=instance, user=new_part["user"], role=new_part["role"]
                    )

        instance.title = validated_data["title"]
        instance.save()

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
