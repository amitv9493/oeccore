from rest_framework import permissions


class Mypermission(permissions.BasePermission):


    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return False