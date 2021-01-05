from ..base.api.permissions import (AllowAny, IsAuthenticated, PermissionComponent, ResourcePermission)


class IsTheSameUser(PermissionComponent):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj=None):
        return request.user.is_authenticated() and request.user.pk == obj.pk


class UserPermissions(ResourcePermission):
    metadata_perms = AllowAny()
    enough_perms = AllowAny()
    global_perms = None
    retrieve_perms = IsTheSameUser()
    update_perms = IsTheSameUser()
    partial_update_perms = IsTheSameUser()
    destroy_perms = IsTheSameUser()
    list_perms = AllowAny()
    login_perms = AllowAny()
    logout_perms = IsAuthenticated()
    passwordchange_perms = AllowAny()
    register_perms = AllowAny()
    registered_list_perms = AllowAny()
    approve_perms = AllowAny()
    permission_group_perms = AllowAny()
    staff_reset_mail_perms = AllowAny()
    reset_password_perms = AllowAny()
    user_clone_perms = AllowAny()
    sms_status_update_perms = AllowAny()
    all_permissions_perms = AllowAny()
    config_perms = AllowAny()


class StaffLoginPermissions(ResourcePermission):
    metadata_perms = AllowAny()
    enough_perms = AllowAny()
    global_perms = None
    retrieve_perms = IsTheSameUser()
    update_perms = IsTheSameUser()
    partial_update_perms = IsTheSameUser()
    destroy_perms = IsTheSameUser()
    send_otp_perms = AllowAny()
    verify_otp_perms = AllowAny()
    resend_otp_perms = AllowAny()
