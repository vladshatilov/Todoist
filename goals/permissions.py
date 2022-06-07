from rest_framework import permissions

from goals.models import BoardParticipant


class BoardPermission(permissions.IsAuthenticated):
    message = 'You are not allowed to view or edit foreign boards.'

    # def has_permission(self, request, view):
    #     return request.user.is_superuser or request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class GoalCategoryPermission(permissions.IsAuthenticated):
    message = 'You are not allowed to view or edit category in foreign boards.'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=request.data.get("board",None)
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=request.data.get("board",None), role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer, ]
        ).exists()

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj.board, role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer, ]
        ).exists()


class GoalPermission(permissions.IsAuthenticated):
    message = 'You are not allowed to view or edit goals in foreign boards.'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.category.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj.category.board, role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer, ]
        ).exists()


class GoalCommentPermission(permissions.IsAuthenticated):
    message = 'You are not allowed to view or edit not your comments.'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
