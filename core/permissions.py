from rest_framework import permissions


class UserAccessPermission(permissions.BasePermission):
    message = 'You are not allowed to view or edit foreign profile.'

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user and request.user.is_authenticated and obj.username == request.user.username


class IsAdminOrOwner(permissions.BasePermission):
    message = 'None of permissions requirements fulfilled.'

    def has_object_permission(self, request, view, obj):
        # return request.user.is_admin()
        return request.user.is_superuser or request.user and request.user.is_authenticated and obj.author_id == request.user


class IsAdminOrOwnerForSelections(permissions.BasePermission):
    message = 'None of permissions requirements fulfilled.'

    # def has_permission(self, request, view):
    #     return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # return request.user.is_admin()
        return request.user.is_superuser or request.user and request.user.is_authenticated and obj.owner == request.user

