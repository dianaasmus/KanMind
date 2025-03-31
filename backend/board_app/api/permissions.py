from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Benutzer 'test' hat überhaupt keinen Zugriff
        if request.user.username == "test":
            return False

        # Bei Lesemethoden (GET, HEAD, OPTIONS) wird Zugriff gewährt
        if request.method in SAFE_METHODS:
            return True

        # Bei Schreibmethoden wird Zugriff nur Staff-Mitgliedern gewährt
        return bool(request.user and request.user.is_staff)
