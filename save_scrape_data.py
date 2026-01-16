from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def save_text_to_pdf(text: str, filename: str = "output.pdf"):
    pdf = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    for paragraph in text.split("\n\n"):
        story.append(Paragraph(paragraph, styles["Normal"]))

    pdf.build(story)
