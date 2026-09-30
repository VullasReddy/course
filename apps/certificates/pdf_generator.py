from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def generate_certificate_pdf(certificate):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        leftMargin=40, rightMargin=40, topMargin=50, bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    brand_style = ParagraphStyle(
        'BrandHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=20, textColor=colors.HexColor('#0B192C'), alignment=TA_CENTER
    )

    title_style = ParagraphStyle(
        'CertTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=28, textColor=colors.HexColor('#0050B3'), alignment=TA_CENTER
    )

    name_style = ParagraphStyle(
        'StudentName', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=32, textColor=colors.HexColor('#0B192C'), alignment=TA_CENTER
    )

    course_style = ParagraphStyle(
        'CourseTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, textColor=colors.HexColor('#00C49F'), alignment=TA_CENTER
    )

    meta_style = ParagraphStyle(
        'MetaText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, textColor=colors.HexColor('#64748B'), alignment=TA_CENTER
    )

    elements = [
        Paragraph("ARSHITH SPRINGBOARD LMS", brand_style),
        Spacer(1, 15),
        Paragraph("CERTIFICATE OF COMPLETION", title_style),
        Spacer(1, 20),
        Paragraph("This is to certify that", meta_style),
        Spacer(1, 15),
        Paragraph(certificate.user.full_name.upper(), name_style),
        Spacer(1, 15),
        Paragraph("has successfully completed the enterprise course requirements for", meta_style),
        Spacer(1, 15),
        Paragraph(certificate.course.title, course_style),
        Spacer(1, 25),
        Paragraph(f"Certificate ID: {certificate.certificate_id} | Issued: {certificate.issue_date.strftime('%B %d, %Y')}", meta_style)
    ]

    doc.build(elements)
    pdf_val = buffer.getvalue()
    buffer.close()
    return pdf_val
