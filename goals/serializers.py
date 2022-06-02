from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField

from core.serializers import UserDetailSerializer
from goals.models import Comment, Goal, GoalCategory


def category_validator(value: GoalCategory, user):
    if value.is_deleted:
        raise serializers.ValidationError("not allowed in deleted category")

    if value.user != user:
        raise serializers.ValidationError("not owner of category")
    # print(f'value - {value}')
    # print(f'value.id - {value.id}')
    return value


# GoalCategory
class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"
        # fields = ["title", "user"]


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


# Goal
class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # category = GoalCategorySerializer(source='GoalCategory')
    category = PrimaryKeyRelatedField(queryset=GoalCategory.objects.all())

    # category = GoalCategorySerializer()
    # category = PrimaryKeyRelatedField(required=False,
    #                                   many=False, queryset=GoalCategory.objects.all())

    # category = serializers.PrimaryKeyRelatedField(
    #         read_only=True,
    #         # default=serializers.CurrentUserDefault()
    #     )
    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def create(self, validated_data):
        category_item = validated_data.pop('category')
        validated_category_item = category_validator(category_item, self.context["request"].user)
        print(category_item)
        print(validated_category_item)
        goal = Goal.objects.create(category_id=validated_category_item.id, **validated_data)
        # for track_data in tracks_data:
        #     Track.objects.create(album=album, **track_data)
        return goal

    # def validate_category(self, value):
    #     category_validator(value, self.context["request"].user)


class GoalSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    # category = GoalCategorySerializer(read_only=True)
    # category = PrimaryKeyRelatedField(read_only=True)

    # category = PrimaryKeyRelatedField(queryset=GoalCategory.objects.all())
    # category = serializers.StringRelatedField(many=False)
    # category = serializers.SlugRelatedField(
    #     many=False,
    #     read_only=True,
    #     slug_field='title'
    # )
    # category = GoalCategorySerializer(source='GoalCategory')

    class Meta:
        model = Comment
        fields = "__all__"
        # read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value):
        category_validator(value, self.context["request"].user)


# Goal Comment
class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # category = GoalCategorySerializer(source='GoalCategory')
    # goal = serializers.PrimaryKeyRelatedField(
    #     read_only=True,
    #     # default=serializers.CurrentUserDefault()
    # )
    # goal = PrimaryKeyRelatedField(queryset=Goal.objects.all())

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
        # fields = ["text", "goal", "user"]


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    # goal = PrimaryKeyRelatedField(queryset=Goal.objects.all())

    class Meta:
        model = Comment
        fields = "__all__"
        # fields = ["text", "goal", "user"]
        read_only_fields = ("id", "created", "updated", "user", "goal")
