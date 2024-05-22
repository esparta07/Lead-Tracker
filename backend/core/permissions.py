from rest_framework import permissions

class ReadOnlyOrAdminPermission(permissions.BasePermission):
    """
    Custom permission to allow read-only access to everyone and restrict
    write access to admins only.
    """

    def has_permission(self, request, view):
        # Allow GET requests to everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Restrict write access to admins only
        return request.user.is_authenticated and request.user.is_admin
