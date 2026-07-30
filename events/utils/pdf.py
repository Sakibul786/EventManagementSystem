from io import BytesIO

from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_attendance_pdf(event):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    story = []

    # ==========================
    # Title
    # ==========================

    story.append(
        Paragraph(
            "<b>EVENT ATTENDANCE REPORT</b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # ==========================
    # Event Information
    # ==========================

    story.append(
        Paragraph(
            f"<b>Event:</b> {event.name}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Date:</b> {event.date}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Time:</b> {event.time}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Location:</b> {event.location}",
            styles["Normal"],
        )
    )

    if event.category:
        story.append(
            Paragraph(
                f"<b>Category:</b> {event.category.name}",
                styles["Normal"],
            )
        )

    story.append(Spacer(1, 0.30 * inch))

    # ==========================
    # Attendance Table
    # ==========================

    table_data = [
        [
            "No",
            "Participant",
            "Email",
            "Status",
        ]
    ]

    total_present = 0

    participants = event.participants.all()

    for index, participant in enumerate(participants, start=1):

        attendance = event.attendance_records.filter(
            participant=participant
        ).first()

        status = "Present"

        if attendance is None or not attendance.is_present:
            status = "Absent"
        else:
            total_present += 1

        table_data.append(
            [
                str(index),
                participant.name,
                participant.email,
                status,
            ]
        )

    table = Table(
        table_data,
        colWidths=[
            0.6 * inch,
            2.2 * inch,
            2.7 * inch,
            1.2 * inch,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.darkblue,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    8,
                ),
            ]
        )
    )

    story.append(table)

    story.append(Spacer(1, 0.30 * inch))

    # ==========================
    # Summary
    # ==========================

    total_registered = participants.count()
    total_absent = total_registered - total_present

    percentage = (
        round(
            (total_present / total_registered) * 100,
            1,
        )
        if total_registered
        else 0
    )

    story.append(
        Paragraph(
            f"<b>Total Registered:</b> {total_registered}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Present:</b> {total_present}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Absent:</b> {total_absent}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Attendance Rate:</b> {percentage}%",
            styles["Normal"],
        )
    )

    document.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response[
        "Content-Disposition"
    ] = f'attachment; filename="{event.name}_Attendance_Report.pdf"'

    return response