from django.urls import path

from goals.views import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView, GoalCommentCreateView, \
    GoalCommentListView, GoalCommentView, GoalCreateView, GoalListView, \
    GoalView

urlpatterns = [
    path('goal_category/create', GoalCategoryCreateView.as_view()),
    path('goal_category/list', GoalCategoryListView.as_view()),
    path("goal_category/<int:pk>", GoalCategoryView.as_view()),
    path('goal/create', GoalCreateView.as_view()),
    path('goal/list', GoalListView.as_view()),
    path("goal/<int:pk>", GoalView.as_view()),
    path('goal_comment/create', GoalCommentCreateView.as_view()),
    path('goal_comment/list', GoalCommentListView.as_view()),
    path("goal_comment/<int:pk>", GoalCommentView.as_view()),
]