from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings
from django.http import FileResponse


def save_pdf(params: dict):
    template = get_template('report_templates/booking_detail_pdf.html')
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    response.seek(0)
    file_name = uuid.uuid4()
    print(file_name)
    return FileResponse(response, as_attachment=True, filename="booking.pdf")
    # try:
    #     with open(str(settings.BASE_DIR)+f'/static/reports/{file_name}.pdf', 'wb+') as output:
    #         pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
    #
    # except Exception as e:
    #     print(e)

    # if pdf.err:
    #     return '', False

