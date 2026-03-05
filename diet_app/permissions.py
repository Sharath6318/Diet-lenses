from rest_framework.permissions import BasePermission

from diet_app.models import User

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if isinstance(obj, User):

            return request.user == obj
        
        return request.user == obj.owner
    
class HasUserProfile(BasePermission):

    message = "User has no Profile"

    def has_permission(self, request, view):
        
        try:

            profile = request.user.profile

            return True

        except:

            return False
            