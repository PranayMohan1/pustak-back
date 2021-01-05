from html import escape
from io import StringIO

from django.core.files.base import File
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa


def html_to_pdf_convert(template, context):
    # stringio read and write strings as a file
    html = template.render(context)
    policy_document_file = NamedTemporaryFile(delete=False)
    # policy_document_file.write(decoded_response)
    # policy_document_file.flush()
    # Changed from file to filename
    pdf = pisa.pisaDocument(StringIO(html), policy_document_file)
    if not pdf.err:
        return File(policy_document_file)
    return False


def convert_html_to_pdf(template, context, document_owner, filename):
    # stringio read and write strings as a file
    html = template.render(context)

    file_obj = NamedTemporaryFile()
    file_obj.name = '/' + document_owner.executive.code + '/' + str(filename)
    pdf = pisa.pisaDocument(StringIO(html.encode("UTF-8")), file_obj)

    if not pdf.err:
        return File(file_obj)
    return False


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO()

    pdf = pisa.pisaDocument(StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
