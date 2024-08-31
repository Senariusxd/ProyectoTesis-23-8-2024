from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from bs4 import BeautifulSoup
from ..models import Interrogatorio, EFaparato
from django.contrib.auth.decorators import login_required

@login_required(login_url="/")
def render_pdf_view(request, pk_paciente, pk_fecha, pk_egeneral):
    # Obtén el interrogatorio que deseas mostrar en el PDF
    interrogatorio = get_object_or_404(Interrogatorio, egeneral__pk=pk_egeneral)

    # Contexto para pasar a la plantilla HTML
    context = {
        'interrogatorio': interrogatorio
    }

    # Renderizar la plantilla HTML
    template_path = 'interrogatorio/interrogatorio.html'  # Nombre de tu plantilla HTML
    template = get_template(template_path)
    html = template.render(context)

    # Crear un objeto HttpResponse con el contenido del PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="interrogatorio.pdf"'

    # Estilos específicos para el PDF (opcional)
    css = """
        <style>
            body {
                font-family: Arial, sans-serif;
                font-size: 12px;
            }
            .centered-title {
                text-align: center;
            }
            .table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            .table th, .table td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            /* Estilos específicos para el PDF */
            @media print {
                .no-pdf {
                    display: none; /* Ocultar elementos con la clase 'no-pdf' al imprimir */
                }
                .table {
                    page-break-inside: avoid; /* Evitar cortar tablas entre páginas */
                }
            }
        </style>
    """
    html = css + html  # Agregar estilos CSS al HTML

    html = remove_buttons(html)

    # Convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Si se ha generado correctamente el PDF, devolverlo como respuesta
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF: %s' % html)
    return response

@login_required(login_url="/")
def remove_buttons(html):
    """
    Función para eliminar botones del HTML generado.
    """
    soup = BeautifulSoup(html, 'html.parser')
    for button in soup.find_all(class_='no-pdf'):
        button.decompose()  # Eliminar elemento del HTML

    return str(soup)

@login_required(login_url="/")
def render_pdf_efaparato(request, pk_paciente, pk_fecha, pk_egeneral):
    efaparato = get_object_or_404(EFaparato, egeneral__pk=pk_egeneral)
    template_path = 'efaparato/efaparato.html'  # Nombre del template HTML
    context = {'efaparato': efaparato}

    # Render template
    template = get_template(template_path)
    html = template.render(context)

    # Estilos específicos para el PDF (opcional)
    css = """
        <style>
            body {
                font-family: Arial, sans-serif;
                font-size: 12px;
            }
            .centered-title {
                text-align: center;
            }
            .table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            .table th, .table td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            /* Estilos específicos para el PDF */
            @media print {
                .no-pdf {
                    display: none; /* Ocultar elementos con la clase 'no-pdf' al imprimir */
                }
                .table {
                    page-break-inside: avoid; /* Evitar cortar tablas entre páginas */
                }
            }
        </style>
    """
    html = css + html  # Agregar estilos CSS al HTML

    # Eliminar elementos no deseados (botones u otros elementos marcados)
    html = remove_elements(html)

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="efaparato.pdf"'

    # Generar el PDF
    pisa_status = pisa.CreatePDF(
        html, dest=response, encoding='utf-8'
    )
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url="/")
def remove_elements(html):
    """
    Función para eliminar elementos no deseados del HTML generado.
    Aquí se puede ajustar para eliminar botones u otros elementos.
    """
    soup = BeautifulSoup(html, 'html.parser')
    # Ejemplo: eliminar elementos con clase 'no-pdf'
    for element in soup.select('.no-pdf'):
        element.decompose()

    # Convertir el soup de nuevo a HTML
    cleaned_html = str(soup)
    return cleaned_html