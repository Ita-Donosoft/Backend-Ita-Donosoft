from io import BytesIO
from re import template
from unittest import result
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_html_to_pdf(template_src, data={}):
    template = get_template(template_src)
    html = template.render(data)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if pdf.err:
        return None

    return HttpResponse(result.getvalue(), content_type='aplication/pdf')
