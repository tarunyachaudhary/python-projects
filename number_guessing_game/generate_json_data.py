from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import json


def generate_user_json_data():
    project_dir = Path(__file__).resolve().parent


    pdf_path = project_dir / "user_data.pdf"

    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4

    # background set
    pdf.setFillColor(colors.black)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    # add header text
    pdf.setFillColor(colors.whitesmoke)
    pdf.setFont("Times-Roman", 30)
    pdf.drawString(210, height - 70, "User data")

    # load json data
    data_path = project_dir / "data.json"
    try:
        with open(data_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError,OSError):
        return {}
        
    y = height - 120
    line_space = 24

    pdf.setFillColor(colors.whitesmoke)
    pdf.setFont("Times-Roman", 15)

    if isinstance(data, dict):
        for name, stats in data.items():
            pdf.drawString(50, y, str(name))
            y -= line_space
            if isinstance(stats, dict):
                for key, value in stats.items():
                    pdf.drawString(80, y, f"{key}: {value}")
                    y -= line_space
            else:
                pdf.drawString(80, y, str(stats))
                y -= line_space
    else:
        pdf.drawString(50, y, json.dumps(data, ensure_ascii=False))


    pdf.save()

    print("user pdf generated successfully!")
