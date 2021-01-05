import logging
from datetime import datetime, date, timedelta
from functools import partial

from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.contrib.auth import logout, get_user_model
from django.core import signing
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from .constants import CONFIG
from .filters import UserBasicFilter
from .models import PasswordResetCode, OTPLogin, User
from .permissions import UserPermissions
from .serializers import UserSerializer, PasswordResetSerializer, UserBasicDataSerializer
from .services import auth_login, auth_password_change, auth_register_user, _parse_data, \
    get_user_from_email_or_mobile, generate_auth_data, user_clone_api
from ..base import response
from ..base.api.pagination import StandardResultsSetPagination
from ..base.api.viewsets import ModelViewSet
from ..base.utils.sms import send_sms_without_save

logger = logging.getLogger(__name__)

parse_password_reset_data = partial(_parse_data, cls=PasswordResetSerializer)


class UserViewSet(ModelViewSet):
    """
    Here we have user login, logout, endpoints.
    """
    queryset = get_user_model().objects.all()
    permission_classes = (UserPermissions,)
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def get_queryset(self):
        queryset = super(UserViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        self.filterset_class = UserBasicFilter
        queryset = self.filter_queryset(queryset)
        return queryset

    @action(detail=False, methods=['GET'])
    def config(self, request):
        data = {}
        parameters = request.query_params.get("parameters", None)
        param_list = parameters.split(",") if parameters else []
        for parameter in param_list:
            if parameter in CONFIG:
                data[parameter] = CONFIG[parameter]
            else:
                data[parameter] = None
        return response.Ok(data)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        return auth_login(request)

    @action(methods=['GET'], detail=False)
    def user_clone(self, request):
        if not request.user.is_authenticated:
            content = {'detail': 'user is not authenticated'}
            return response.BadRequest(content)
        return response.Ok(user_clone_api(request.user))

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return response.Ok({"detail": "Successfully logged out."})

    @action(detail=False, methods=['POST'])
    def password_change(self, request):
        data = auth_password_change(request)
        user, new_password = request.user, data.get('new_password')
        if user.check_password(data.get('old_password')):
            user.set_password(new_password)
            user.save()
            content = {'success': 'Password changed successfully.'}
            return response.Ok(content)
        else:
            content = {'detail': 'Old password is incorrect.'}
            return response.BadRequest(content)

    @action(detail=False, methods=['POST'])
    def register(self, request):
        data = auth_register_user(request)
        return response.Created(data)

    @action(detail=True, methods=['POST'])
    def deactivate(self, request):
        user = self.get_object()
        is_active = request.data('is_active')
        user.is_active = is_active
        user.save()
        content = {'success': 'User Deactivated successfully.'}
        return response.Ok(content)

    @action(detail=False, methods=['POST'])
    def user_reset_mail(self, request):
        data = parse_password_reset_data(request.data)
        username = data.get('username')
        user, email_user, mobile_user = get_user_from_email_or_mobile(username)
        if not email_user and not mobile_user:
            return response.BadRequest({'detail': 'User does not exists.'})
        if user:
            try:
                email = user.email
                password_reset_code = PasswordResetCode.objects.create_reset_code(user)
                password_reset_code.send_password_reset_email()
                message = "We have sent a password reset link to the {}. Use that link to set your new password".format(
                    email)
                return response.Ok({"detail": message})
            except get_user_model().DoesNotExist:
                message = "Email '{}' is not registered with us. Please provide a valid email id".format(email)
                message_dict = {'detail': message}
                return response.BadRequest(message_dict)
            except Exception:
                message = "Unable to send password reset link to email-id- {}".format(email)
                message_dict = {'detail': message}
                logger.exception(message)
                return response.BadRequest(message_dict)
        else:
            message = {'detail': 'User for this staff does not exist'}
            return response.BadRequest(message)

    @action(detail=False, methods=['POST'])
    def reset_password(self, request):
        code = request.data.get('code')
        password = request.data.get('password')
        if code:
            try:
                password_reset_code = PasswordResetCode.objects.get(code=code.encode('utf8'))
                uid = force_text(urlsafe_base64_decode(password_reset_code.uid))
                password_reset_code.user = get_user_model().objects.get(id=uid)
            except:
                message = 'Unable to verify user.'
                message_dict = {'detail': message}
                return response.BadRequest(message_dict)
            # verify signature with the help of timestamp and previous password for one secret urls of password reset.
            else:
                signer = signing.TimestampSigner()
                max_age = settings.PASSWORD_RESET_TIME
                l = (password_reset_code.user.password, password_reset_code.timestamp, password_reset_code.signature)
                try:
                    signer.unsign(':'.join(l), max_age=max_age)
                except (signing.BadSignature, signing.SignatureExpired):
                    logger.info('Session Expired')
                    message = 'Password reset link expired. Please re-generate password reset link. '
                    message_dict = {'detail': message}
                    return response.BadRequest(message_dict)
            password_reset_code.user.set_password(password)
            password_reset_code.user.save()
            message = "Password Created successfully"
            message_dict = {'detail': message}
            return response.Ok({"success": message_dict})
        else:
            message = {'detail': 'Password reset link expired. Please re-generate password reset link. '}
            return response.BadRequest(message)

    @action(detail=False, methods=['POST'])
    def resend_otp(self, request):
        import datetime
        mobile = request.data.get("mobile")
        user_model = get_user_model()
        user = user_model.objects.filter(is_active=True, mobile=mobile).first()
        if user:
            timestamp = datetime.datetime.now() - datetime.timedelta(minutes=15)
            login_obj = OTPLogin.objects.filter(mobile=mobile, is_active=True, modified_at__gte=timestamp,
                                                resend_counter__gt=0).first()
            if login_obj:
                send_sms_without_save(mobile, "Your OTP for My Fitnezz Login is " + str(
                    login_obj.otp) + ". It is valid for next 10 minutes.")
                login_obj.resend_counter = login_obj.resend_counter - 1
                login_obj.save()
                return response.Ok({"detail": "OTP resent successfully"})
            else:
                return response.BadRequest(
                    {"detail": "Maximum retries have been exceeded. Please retry after 15 minutes."})
        else:
            return response.BadRequest({"detail": "No User exists with mobile no: " + str(mobile)})

    @action(detail=False, methods=['POST'])
    def send_otp(self, request):
        mobile = request.data.get("mobile")
        user_model = get_user_model()
        user = user_model.objects.filter(is_active=True, mobile=mobile).first()
        if user:
            otp = self.get_random_number(6)
            OTPLogin.objects.filter(mobile=mobile, modified_at__lt=date.today(), is_active=True).delete()
            login_obj = OTPLogin.objects.filter(mobile=mobile, is_active=True, modified_at__gte=date.today()).first()
            if login_obj:
                counter = login_obj.counter - 1
                if counter > 0:
                    OTPLogin.objects.filter(mobile=mobile, is_active=True, modified_at__gte=date.today()).update(
                        otp=otp, is_active=True, counter=counter, resend_counter=25, modified_at=datetime.now())
            else:
                counter = 25
                OTPLogin.objects.create(mobile=mobile, otp=otp)
            if counter > 0:
                send_sms_without_save(mobile, "Your OTP for My Fitnezz Login is " + str(
                    otp) + ". It is valid for next 10 minutes.")
                return response.Ok({"detail": "OTP sent successfully"})
            else:
                return response.BadRequest(
                    {"detail": "Max tries for OTP exceeded. Kindly try again tommorow or login with password"})
        else:
            return response.BadRequest({"detail": "No User exists with mobile no: " + str(mobile)})

    @action(detail=False, methods=['POST'])
    def verify_otp(self, request):
        mobile = request.data.get("mobile")
        otp = request.data.get("otp")
        user_model = get_user_model()
        user = user_model.objects.filter(is_active=True, mobile=mobile).first()
        if user:
            timestamp = datetime.now() - timedelta(minutes=15)
            login_obj = OTPLogin.objects.filter(mobile=mobile, otp=otp, is_active=True,
                                                modified_at__gte=timestamp).first()
            if login_obj:
                login_obj.is_active = False
                login_obj.save()
                auth_data = generate_auth_data(request, user)
                return response.Ok(auth_data)
            else:
                return response.BadRequest({"detail": "Invalid OTP used. Please Check!!"})
        else:
            return response.BadRequest({"detail": "No Such User with mobile no: " + str(mobile) + " exists."})

    def get_random_number(self, N):
        from random import randint
        '''
        :param N: No of Digits
        :return: Random number of N digit
        '''

        range_start = 10 ** (N - 1)
        range_end = (10 ** N) - 1
        return randint(range_start, range_end)

    @action(methods=['GET'], detail=False, pagination_class=StandardResultsSetPagination)
    def employee_list(self, request):
        queryset = User.objects.filter(is_active=True)
        self.filterset_class = UserBasicFilter
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(UserBasicDataSerializer(page, many=True).data)
        return response.Ok(UserBasicDataSerializer(queryset, many=True).data)
