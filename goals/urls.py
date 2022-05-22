from django.urls import path

from goals.views import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView

urlpatterns = [
    path('goal_category/create', GoalCategoryCreateView.as_view()),
    path('goal_category/list', GoalCategoryListView.as_view()),
    path("goal_category/<int:pk>", GoalCategoryView.as_view()),
]