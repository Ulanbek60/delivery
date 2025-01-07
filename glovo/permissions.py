from rest_framework import permissions


class CheckUserCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'owner':
            return True
        return False

class CheckReviewUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'client':
            return True
        return False


class CheckCourierUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'courier':
            return True
        return False


class CheckReviewEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user_name


class CheckOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsStoreOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.store.owner == request.user


