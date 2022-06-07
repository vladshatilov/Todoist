from django.db import transaction
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from goals.filters import CommentFilter, GoalDateFilter
from goals.models import Board, Comment, Goal, GoalCategory
from goals.permissions import BoardPermission, GoalCategoryPermission, GoalCommentPermission, GoalPermission
from goals.serializers import BoardCreateSerializer, BoardListSerializer, BoardSerializer, \
    GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCommentCreateSerializer, \
    GoalCommentSerializer, GoalCreateSerializer, GoalSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [GoalCategoryPermission]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["board", "user"]
    ordering_fields = ["title", "created", "board"]
    ordering = ["title"]
    search_fields = ["title", "board"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__board_participants__user=self.request.user,
            is_deleted=False  # , board__is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermission]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__board_participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


    #
    # Goals part
    #
class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["due_date", "priority"]
    ordering = ["priority", "due_date"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__board_participants__user=self.request.user
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, GoalPermission]

    def get_queryset(self):
        return Goal.objects.filter(category__board__board_participants__user=self.request.user)


    #
    # Comment part
    #
class GoalCommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = CommentFilter
    search_fields = ["text"]
    ordering_fields = ["created"]
    ordering = ["-created"]

    def get_queryset(self):
        return Comment.objects.filter(
            user=self.request.user
        )


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = GoalCommentSerializer
    permission_classes = [GoalCommentPermission]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


    #
    # Board part
    #
class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination
    # filter_backends = [
    #     DjangoFilterBackend,
    #     filters.OrderingFilter,
    #     filters.SearchFilter,
    # ]
    # filterset_class = CommentFilter
    # search_fields = ["text"]
    ordering_fields = ["title"]
    ordering = ["-created"]

    def get_queryset(self):
        return Board.objects.filter(
            board_participants__user=self.request.user
        )


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    serializer_class = BoardSerializer
    permission_classes = [BoardPermission]

    def get_queryset(self):
        return Board.objects.filter(board_participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance
