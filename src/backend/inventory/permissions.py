from ..base.api.permissions import (AllowAny, IsAuthenticated,
                                    IsSuperUser, PermissionComponent,
                                    ResourcePermission)


class IsTheSameUser(PermissionComponent):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj=None):
        return request.user.is_authenticated() and request.user.pk == obj.pk


class BookCategoryPermissions(ResourcePermission):
    metadata_perms = AllowAny()
    enough_perms = AllowAny()
    global_perms = None
    retrieve_perms = AllowAny()
    create_perms = AllowAny()
    update_perms = AllowAny()
    partial_update_perms = AllowAny()
    destroy_perms = AllowAny()
    list_perms = AllowAny()

class BookProductPermissions(ResourcePermission):
    metadata_perms = AllowAny()
    enough_perms = AllowAny()
    global_perms = None
    retrieve_perms = AllowAny()
    create_perms = AllowAny()
    update_perms = AllowAny()
    partial_update_perms = AllowAny()
    destroy_perms = AllowAny()
    list_perms = AllowAny()
    book_approval_perms = AllowAny()

class ApprovalPermissions(ResourcePermission):
    metadata_perms = AllowAny()
    enough_perms = AllowAny()
    global_perms = None
    retrieve_perms = AllowAny()
    create_perms = AllowAny()
    update_perms = AllowAny()
    partial_update_perms = AllowAny()
    destroy_perms = AllowAny()
    list_perms = AllowAny()
    book_approval_perms=AllowAny()