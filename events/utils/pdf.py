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

from events.models import OfflineAttendance


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

    # =====================================
    # Title
    # =====================================

    story.append(
        Paragraph(
            "<b>EVENT ATTENDANCE REPORT</b>",
            styles["Title"],
        )
    )

    story.append(
        Spacer(
            1,
            0.25 * inch,
        )
    )

    # =====================================
    # Event Information
    # =====================================

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

    story.append(
        Spacer(
            1,
            0.30 * inch,
        )
    )

    # =====================================
    # Attendance Table
    # =====================================

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

    for index, participant in enumerate(
        participants,
        start=1,
    ):

        attendance = event.attendance_records.filter(
            participant=participant,
        ).first()

        status = "Absent"

        if attendance and attendance.is_present:

            status = "Present"
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
            2.8 * inch,
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
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
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

    story.append(
        Spacer(
            1,
            0.35 * inch,
        )
    )

    # =====================================
    # Summary
    # =====================================

    offline_attendance, created = OfflineAttendance.objects.get_or_create(
        event=event
    )

    # =====================================
    # Online Statistics
    # =====================================

    online_registered = participants.count()

    online_present = total_present

    online_absent = (
        online_registered -
        online_present
    )

    # =====================================
    # Offline Statistics
    # =====================================

    offline_present = offline_attendance.present

    offline_registered = event.offline_participants

    offline_absent = max(
    0,
        offline_registered - offline_present
    )


    # =====================================
    # Overall Statistics
    # =====================================

    total_registered = (
        online_registered +
        offline_registered
    )

    total_present = (
        online_present +
        offline_present
    )

    total_absent = (
        online_absent +
        offline_absent
    )

    attendance_percentage = (
        round(
            (total_present / total_registered) * 100,
            1,
        )
        if total_registered > 0
        else 0
    )

    summary_data = [

        [
            "Statistics",
            "Count",
        ],

        [
            "Online Registered",
            str(online_registered),
        ],

        [
            "Offline Registered",
            str(offline_registered),
        ],

        [
            "Total Registered",
            str(total_registered),
        ],

        [
            "Online Present",
            str(online_present),
        ],

        [
            "Offline Present",
            str(offline_present),
        ],

        [
            "Total Present",
            str(total_present),
        ],

        [
            "Online Absent",
            str(online_absent),
        ],

        [
            "Offline Absent",
            str(offline_absent),
        ],

        [
            "Total Absent",
            str(total_absent),
        ],

        [
            "Attendance Percentage",
            f"{attendance_percentage} %",
        ],

    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            3.2 * inch,
            2 * inch,
        ],
    )

    summary_table.setStyle(
        TableStyle(

            [

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.darkgreen,
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
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

    story.append(summary_table)

    document.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response[
        "Content-Disposition"
    ] = (
        f'attachment; '
        f'filename="{event.name}_Attendance_Report.pdf"'
    )

    return response