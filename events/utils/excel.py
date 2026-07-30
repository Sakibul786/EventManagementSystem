from django.http import HttpResponse

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment


def generate_attendance_excel(event):

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Attendance Report"

    # ==========================
    # Title
    # ==========================

    worksheet.merge_cells("A1:D1")

    title = worksheet["A1"]
    title.value = "EVENT ATTENDANCE REPORT"
    title.font = Font(size=16, bold=True)
    title.alignment = Alignment(horizontal="center")

    # ==========================
    # Event Information
    # ==========================

    worksheet["A3"] = "Event"
    worksheet["B3"] = event.name

    worksheet["A4"] = "Date"
    worksheet["B4"] = str(event.date)

    worksheet["A5"] = "Time"
    worksheet["B5"] = str(event.time)

    worksheet["A6"] = "Location"
    worksheet["B6"] = event.location

    if event.category:
        worksheet["A7"] = "Category"
        worksheet["B7"] = event.category.name

    # ==========================
    # Table Header
    # ==========================

    start_row = 9

    headers = [
        "No",
        "Participant",
        "Email",
        "Status",
    ]

    fill = PatternFill(
        fill_type="solid",
        start_color="1F4E78",
        end_color="1F4E78",
    )

    for column, header in enumerate(headers, start=1):

        cell = worksheet.cell(
            row=start_row,
            column=column,
        )

        cell.value = header
        cell.font = Font(
            bold=True,
            color="FFFFFF",
        )
        cell.fill = fill
        cell.alignment = Alignment(horizontal="center")

    # ==========================
    # Attendance Data
    # ==========================

    total_present = 0

    row = start_row + 1

    for index, participant in enumerate(
        event.participants.all(),
        start=1,
    ):

        attendance = event.attendance_records.filter(
            participant=participant
        ).first()

        status = "Present"

        if attendance is None or not attendance.is_present:
            status = "Absent"
        else:
            total_present += 1

        worksheet.cell(row=row, column=1).value = index
        worksheet.cell(row=row, column=2).value = participant.name
        worksheet.cell(row=row, column=3).value = participant.email
        worksheet.cell(row=row, column=4).value = status

        row += 1

    # ==========================
    # Summary
    # ==========================

    total_registered = event.participants.count()
    total_absent = total_registered - total_present

    attendance_percentage = (
        round(
            total_present / total_registered * 100,
            1,
        )
        if total_registered
        else 0
    )

    row += 2

    worksheet.cell(row=row, column=1).value = "Total Registered"
    worksheet.cell(row=row, column=2).value = total_registered

    row += 1

    worksheet.cell(row=row, column=1).value = "Present"
    worksheet.cell(row=row, column=2).value = total_present

    row += 1

    worksheet.cell(row=row, column=1).value = "Absent"
    worksheet.cell(row=row, column=2).value = total_absent

    row += 1

    worksheet.cell(row=row, column=1).value = "Attendance Rate"
    worksheet.cell(row=row, column=2).value = f"{attendance_percentage}%"

    # ==========================
    # Column Width
    # ==========================

    worksheet.column_dimensions["A"].width = 10
    worksheet.column_dimensions["B"].width = 30
    worksheet.column_dimensions["C"].width = 35
    worksheet.column_dimensions["D"].width = 18

    # ==========================
    # Response
    # ==========================

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    response[
        "Content-Disposition"
    ] = (
        f'attachment; '
        f'filename="{event.name}_Attendance_Report.xlsx"'
    )

    workbook.save(response)

    return response