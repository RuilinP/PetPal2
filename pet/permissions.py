from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken

class IsShelterUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and has a valid token
        if not request.user.is_authenticated:
            return False

        # Check if the user type is 'shelter'        
        if hasattr(request.user, 'seeker'):
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # Check if the shelter user's ID corresponds to the "shelter" field of the pet
        if hasattr(request.user, 'seeker'):
            return False
        return (
            request.user.is_authenticated 
            and obj.shelter == request.user.id
        )