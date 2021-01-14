import base64
import os
import random
from csv import DictWriter
from string import ascii_letters

import boto3
from django.conf import settings
from django.template.loader import get_template

from . import response
from .utils import email
from .utils import timezone, pdf_document
# from ..constants.hard_data import CONST_GLOBAL_PRACTICE, CONST_MAIL_BODY
# from ..constants.hard_data import CONST_REPORT_MAIL
# from ..customer.models import Customer, GeneratedPdf
# from ..customer.serializers import CustomerSerializer
# from ..practice.models import Communications, Practice, PracticePrintSettings
# from ..practice.models import PracticeStaff
# from ..practice.models import PracticeUserPermissions
# from ..practice.serializers import PracticeSerializer, CommunicationSerializer, PracticeStaffSerializer, \
#     PracticeBasicDataSerializer


# def get_practice_name(practice_id):
#     if practice_id:
#         instance = Practice.objects.filter(id=practice_id).first()
#         return instance.name
#     return CONST_GLOBAL_PRACTICE
#
#
# def get_mail_body(practice_id, report_name):
#     name = get_practice_name(practice_id)
#     return CONST_MAIL_BODY.format(report_name, name)


def create_update_record(request, serializer_class, model_class):
    request_data = request.data.copy() if not isinstance(request, dict) else request
    data_id = request_data.pop('id', None)
    if data_id:
        data_obj = model_class.objects.get(id=data_id)
        serializer = serializer_class(instance=data_obj, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        update_object = serializer.save()
        return serializer_class(instance=update_object).data
    serializer = serializer_class(data=request_data)
    serializer.is_valid(raise_exception=True)
    update_object = serializer.save()
    return serializer_class(instance=update_object).data

#
# def generate_pdf(pdf_type, sub_type, model, serializer, model_id, practice, patient, doctor, template, name,
#                  extra_data=None):
#     page_settings = PracticePrintSettings.objects.filter(type=pdf_type, sub_type=sub_type, practice=practice).order_by(
#         "-modified_at").values()
#     if page_settings:
#         page_settings = page_settings[0]
#     else:
#         page_settings = {}
#     if patient:
#         patient_data = CustomerSerializer(Customer.objects.get(id=patient)).data
#     else:
#         patient_data = {}
#     if doctor:
#         doctor_data = PracticeStaffSerializer(PracticeStaff.objects.get(id=doctor)).data
#     else:
#         doctor_data = {}
#     if practice:
#         practice_data = PracticeBasicDataSerializer(Practice.objects.get(id=practice)).data
#     else:
#         practice_data = {}
#     if model_id:
#         model_data = serializer(instance=model.objects.get(id=model_id)).data
#     else:
#         model_data = None
#     if model_data is None:
#         model_data = model
#     logo = None
#     if page_settings and page_settings['logo_include']:
#         logo = page_settings['logo_path']
#         if logo and settings.SERVER == "PRODUCTION":
#             s3_config = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
#             data = s3_config.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=logo.replace('+', ' '))
#             logo = base64.b64encode(data['Body'].read()).decode('ascii')
#         elif logo:
#             png_file = open(os.path.join(settings.BASE_DIR, 'media', logo), 'rb')
#             logo = base64.b64encode(png_file.read()).decode('ascii')
#     pdf_data = {
#         'logo': logo,
#         'page_settings': page_settings,
#         'data': model_data,
#         'extra_data': extra_data,
#         'patient': patient_data,
#         'doctor': doctor_data,
#         'practice': practice_data,
#         'time': timezone.now_local().strftime("%d/%m/%Y %I:%M %p")
#     }
#     template = get_template(template)
#     pdf = pdf_document.html_to_pdf_convert(template, pdf_data)
#     letters = ascii_letters
#     random_str = ''.join(random.choice(letters) for _ in range(4))
#     if model_id:
#         pdf_obj, _ = GeneratedPdf.objects.get_or_create(name=name + str(model_id))
#         pdf_obj.report.save("%s-%s.pdf" % (random_str, model_id), pdf)
#     else:
#         pdf_obj, _ = GeneratedPdf.objects.get_or_create(name=name + str(patient))
#         pdf_obj.report.save("%s-%s.pdf" % (random_str, patient), pdf)
#     if not settings.SERVER == "PRODUCTION":
#         pdf.flush()
#     return pdf_obj
#
#
# def mail_file(patient_name, mail_to, pdf_obj, practice, report_name):
#     html = get_template('email_content.html')
#     if practice:
#         communications = Communications.objects.filter(practice=practice, is_active=True)
#         if not communications.exists():
#             return {"error": True, "detail": "Please set details in communication settings"}
#         practice_details = PracticeSerializer(Practice.objects.filter(id=practice).first()).data
#         communication_details = CommunicationSerializer(communications.order_by("-id").first()).data
#         data = {"practice": practice_details, "communications": communication_details, "name": patient_name,
#                 "report_name": report_name, "base_url": settings.DOMAIN + settings.MEDIA_URL}
#         if pdf_obj:
#             html_content = html.render(data)
#             subject = report_name + " from " + practice_details["name"]
#             file = pdf_obj.report
#             email.send(mail_to, subject, html_content, "", [file])
#             return {"error": False, "detail": "Mail Sent Successfully"}
#         return {"error": True, "detail": "Failed to generate mail document"}
#     return {"error": True, "detail": "Invalid Clinic Selected"}
#
#
# def common_function(self, request, patient_id, practice_id, get_serializer, post_serializer, model, sort_on):
#     if request.method == 'GET':
#         data = model.objects.filter(is_active=True)
#         if patient_id:
#             data = data.filter(patient=patient_id)
#         if practice_id:
#             data = data.filter(practice=practice_id)
#         if sort_on:
#             data = data.order_by(sort_on, '-id')
#         page = self.paginate_queryset(data)
#         if page is not None:
#             return self.get_paginated_response(get_serializer(page, many=True).data)
#         return response.Ok(get_serializer(data, many=True).data)
#     if patient_id:
#         patient_instance = Customer.objects.get(id=patient_id)
#         update_response = update_patient_extra_details(request, post_serializer, patient_instance, model)
#         return response.Ok(update_response) if update_response else response.BadRequest(
#             {'detail': 'Send patient with data'})
#     return response.BadRequest({'detail': 'Send patient with data'})
#
#
# def update_patient_extra_details(request, serializer_class, instance, model_class):
#     new_data_request = request.data.copy() if not isinstance(request, dict) else request
#     new_data_request['patient'] = instance.pk if instance else None
#     file_tags_id = new_data_request.pop('id', None)
#     if file_tags_id:
#         file_tags_object = model_class.objects.get(id=file_tags_id)
#         serializer = serializer_class(instance=file_tags_object, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         update_object = serializer.save()
#         return serializer_class(instance=update_object).data
#     serializer = serializer_class(data=new_data_request)
#     serializer.is_valid(raise_exception=True)
#     update_object = serializer.save()
#     return serializer_class(instance=update_object).data
#
#
# def dict_to_mail(data, report_name, mail_to, subject, body):
#     if len(data) > 0:
#         header = tuple(data[0].keys())
#         path = os.path.join(settings.MEDIA_ROOT, report_name + ".csv")
#         is_superuser = PracticeStaff.objects.filter(user__email=mail_to, is_active=True, user__is_active=True,
#                                                     user__is_superuser=True).first()
#         staff = PracticeStaff.objects.filter(user__email=mail_to, is_active=True, user__is_active=True)
#         allowed = PracticeUserPermissions.objects.filter(codename=CONST_REPORT_MAIL, is_active=True,
#                                                          staff__user__email=mail_to).count()
#         if is_superuser or (staff.count() > 0 and allowed):
#             staff_name = staff.first().user.first_name
#             body = "Dear <b>" + staff_name + "</b>,<br/><br/>" + body
#             with open(path, 'w') as outfile:
#                 writer = DictWriter(outfile, header)
#                 writer.writeheader()
#                 writer.writerows(data)
#             email.send(mail_to, subject, body, "", [open(path, 'r')])
#             os.remove(path)
#             return False, "Mail Sent Successfully to " + mail_to
#         if staff.count() == 0:
#             return True, "No staff exists with this mail"
#         return True, "You do not have permissions to send reports on mail"
#     return True, "No data available for mailing"
