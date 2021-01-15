from ..base.api.permissions import (AllowAny, IsAuthenticated,
                                    IsSuperUser, PermissionComponent,
                                    ResourcePermission)


class SettingsPermissions(ResourcePermission):
    metadata_perms = AllowAny()
    enough_perms = AllowAny()
    global_perms = None
    retrieve_perms = AllowAny()
    create_perms = AllowAny()
    update_perms = AllowAny()
    partial_update_perms = AllowAny()
    destroy_perms = AllowAny()
    list_perms = AllowAny()