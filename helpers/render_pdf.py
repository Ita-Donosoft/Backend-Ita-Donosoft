from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_html_to_pdf(template_src, data={}):
    """This function renders a template of html to pdf.

    Args:
        template_src (str):
            This var is the route of the template.
        data (dict, optional): 
            This is the data to incorporate in the template. Defaults to {}.

    Returns:
        HttpResponse: 
            If there is no error it generates a http response with the PDF document.
            If there is an error it returns None.
    """
    template = get_template(template_src)
    html = template.render(data)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if pdf.err:
        return None

    return HttpResponse(result.getvalue(), content_type='aplication/pdf')
