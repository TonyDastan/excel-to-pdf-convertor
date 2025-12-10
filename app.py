import io
import os
import shutil
from datetime import datetime

import pandas as pd
from flask import Flask, jsonify, render_template, request, send_file
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"xlsx", "xls", "csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert_excel_to_pdf():
    try:
        # Get form data
        file = request.files.get("file")
        title = request.form.get("title", "ATTENDANCE REPORT")
        subtitle = request.form.get("subtitle", "")
        report_date = request.form.get("report_date", "")

        print("=" * 60)
        print(f"DEBUG - Report date received: '{report_date}'")
        print(f"DEBUG - Report date type: {type(report_date)}")
        print(f"DEBUG - Report date length: {len(report_date) if report_date else 0}")
        print(
            f"DEBUG - Report date stripped: '{report_date.strip() if report_date else ''}'"
        )
        print("=" * 60)

        if not file or not allowed_file(file.filename):
            return jsonify(
                {"error": "Invalid file format. Please upload Excel or CSV files."}
            ), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Read Excel/CSV file
        try:
            if filepath.endswith(".csv"):
                df = pd.read_csv(filepath)
            else:
                # Read the Excel file without automatic header detection
                df_raw = pd.read_excel(filepath, header=None)

                # Find the header row (usually has EmployeeName)
                header_row = 0
                for idx, row in df_raw.iterrows():
                    row_str = " ".join(str(v) for v in row if pd.notna(v))
                    if "EmployeeName" in row_str or "employee" in row_str.lower():
                        header_row = idx
                        break

                # Read with proper header
                df = pd.read_excel(filepath, header=header_row)

            # Clean up the dataframe
            # Remove rows that are all NaN
            df = df.dropna(how="all")

            # Remove columns that are completely empty or contain "Unnamed"
            df = df.loc[:, ~df.columns.str.contains("Unnamed", case=False, na=False)]

            # Reset index
            df = df.reset_index(drop=True)

            # Remove any rows where all values are NaN
            df = df.dropna(how="all")

        except Exception as e:
            return jsonify({"error": f"Error reading file: {str(e)}"}), 400

        # Generate PDF
        pdf_buffer = io.BytesIO()

        # Format title and subtitle - title includes branch name + "DAILY STAFF ATTENDANCE", subtitle is date
        branch_name = os.path.splitext(filename)[0].upper()

        # Create PDF filename with branch name and date (only if date provided)
        print(f"DEBUG - Checking if report_date exists: {bool(report_date)}")
        print(
            f"DEBUG - Checking if report_date.strip() exists: {bool(report_date.strip()) if report_date else False}"
        )

        if report_date and report_date.strip():
            try:
                print(f"DEBUG - Attempting to parse date: '{report_date}'")
                date_obj = datetime.strptime(report_date, "%Y-%m-%d")
                date_str = date_obj.strftime("%d-%m-%Y")
                pdf_filename = f"{branch_name}_{date_str}.pdf"
                print(f"DEBUG - SUCCESS! PDF filename created: '{pdf_filename}'")
            except Exception as e:
                print(f"DEBUG - ERROR creating filename: {e}")
                print(f"DEBUG - Exception type: {type(e).__name__}")
                pdf_filename = f"{branch_name}.pdf"
        else:
            pdf_filename = f"{branch_name}.pdf"
            print(
                f"DEBUG - No valid date provided, using filename without date: '{pdf_filename}'"
            )
        formatted_title = f"{branch_name} DAILY STAFF ATTENDANCE"
        formatted_subtitle = "LATE COMMERS AND ABSENTEEISM"
        if report_date and report_date.strip():
            try:
                date_obj = datetime.strptime(report_date, "%Y-%m-%d")
                formatted_subtitle = (
                    f"LATE COMMERS AND ABSENTEEISM {date_obj.strftime('%d %B %Y')}"
                )
            except:
                formatted_subtitle = f"LATE COMMERS AND ABSENTEEISM {report_date}"

        generate_attendance_pdf(
            pdf_buffer, df, formatted_title, formatted_subtitle, report_date
        )
        pdf_buffer.seek(0)

        # Save to output folder first
        output_path = os.path.join(OUTPUT_FOLDER, pdf_filename)
        with open(output_path, "wb") as f:
            f.write(pdf_buffer.read())

        print("=" * 60)
        print(f"DEBUG - FINAL: Sending file with name: '{pdf_filename}'")
        print(f"DEBUG - Saved to: '{output_path}'")
        print("=" * 60)

        # Read the saved file and create response with explicit headers
        with open(output_path, "rb") as f:
            pdf_data = f.read()

        from flask import Response, make_response

        response = make_response(pdf_data)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = (
            f'attachment; filename="{pdf_filename}"'
        )
        response.headers["Content-Length"] = len(pdf_data)
        return response

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500


@app.route("/batch-convert", methods=["POST"])
def batch_convert_excel_to_pdf():
    """Convert multiple Excel files to PDF in batch"""
    try:
        # Get form data
        files = request.files.getlist("files[]")
        subtitle = request.form.get("subtitle", "")
        report_date = request.form.get("report_date", "")

        if not files:
            return jsonify({"error": "No files uploaded"}), 400

        # Create batch output folder
        batch_folder = os.path.join(
            OUTPUT_FOLDER, f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        os.makedirs(batch_folder, exist_ok=True)

        pdf_files = []
        errors = []

        for file in files:
            try:
                if not file or not allowed_file(file.filename):
                    errors.append(f"{file.filename}: Invalid file format")
                    continue

                # Extract just the filename (remove folder paths from webkitdirectory)
                # file.filename might be like "folder/subfolder/filename.xlsx"
                filename = secure_filename(os.path.basename(file.filename))
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                # Get title from filename (without extension)
                title = os.path.splitext(filename)[0].upper()

                # Read Excel/CSV file
                try:
                    if filepath.endswith(".csv"):
                        df = pd.read_csv(filepath)
                    else:
                        # Read the Excel file without automatic header detection
                        df_raw = pd.read_excel(filepath, header=None)

                        # Find the header row
                        header_row = 0
                        for idx, row in df_raw.iterrows():
                            row_str = " ".join(str(v) for v in row if pd.notna(v))
                            if (
                                "EmployeeName" in row_str
                                or "employee" in row_str.lower()
                            ):
                                header_row = idx
                                break

                        # Read with proper header
                        df = pd.read_excel(filepath, header=header_row)

                    # Clean up the dataframe
                    df = df.dropna(how="all")
                    df = df.loc[
                        :, ~df.columns.str.contains("Unnamed", case=False, na=False)
                    ]
                    df = df.reset_index(drop=True)
                    df = df.dropna(how="all")

                    # Format title and subtitle - title includes branch name + "DAILY STAFF ATTENDANCE", subtitle is date
                    branch_name = os.path.splitext(filename)[0].upper()
                    formatted_title = f"{branch_name} DAILY STAFF ATTENDANCE"
                    formatted_subtitle = "LATE COMMERS AND ABSENTEEISM"
                    if report_date and report_date.strip():
                        try:
                            date_obj = datetime.strptime(report_date, "%Y-%m-%d")
                            formatted_subtitle = f"LATE COMMERS AND ABSENTEEISM {date_obj.strftime('%d %B %Y')}"
                        except:
                            formatted_subtitle = (
                                f"LATE COMMERS AND ABSENTEEISM {report_date}"
                            )

                    # Generate PDF
                    pdf_buffer = io.BytesIO()
                    generate_attendance_pdf(
                        pdf_buffer, df, formatted_title, formatted_subtitle, report_date
                    )
                    pdf_buffer.seek(0)

                    # Save PDF with branch name and date (only if date provided)
                    if report_date and report_date.strip():
                        try:
                            date_obj = datetime.strptime(report_date, "%Y-%m-%d")
                            date_str = date_obj.strftime("%d-%m-%Y")
                            pdf_filename = f"{branch_name}_{date_str}.pdf"
                        except:
                            pdf_filename = f"{branch_name}.pdf"
                    else:
                        pdf_filename = f"{branch_name}.pdf"
                    pdf_path = os.path.join(batch_folder, pdf_filename)

                    with open(pdf_path, "wb") as f:
                        f.write(pdf_buffer.read())

                    pdf_files.append(pdf_path)

                except Exception as e:
                    errors.append(f"{filename}: {str(e)}")

            except Exception as e:
                errors.append(f"{file.filename}: {str(e)}")

        if not pdf_files:
            return jsonify(
                {"error": "No PDFs were generated. " + "; ".join(errors)}
            ), 400

        # Create ZIP file
        import zipfile

        zip_filename = (
            f"attendance_reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        )
        zip_path = os.path.join(OUTPUT_FOLDER, zip_filename)

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for pdf_file in pdf_files:
                arcname = os.path.basename(pdf_file)
                zipf.write(pdf_file, arcname)

        # Return ZIP file with explicit headers
        with open(zip_path, "rb") as f:
            zip_data = f.read()

        from flask import Response, make_response

        response = make_response(zip_data)
        response.headers["Content-Type"] = "application/zip"
        response.headers["Content-Disposition"] = (
            f'attachment; filename="{zip_filename}"'
        )
        response.headers["Content-Length"] = len(zip_data)
        return response

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500


def generate_attendance_pdf(pdf_buffer, df, title, subtitle, report_date=None):
    """Generate PDF with attendance data and color coding"""

    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        rightMargin=0.3 * inch,
        leftMargin=0.3 * inch,
        topMargin=0.4 * inch,
        bottomMargin=0.4 * inch,
    )

    story = []
    styles = getSampleStyleSheet()

    # Try to use Calibri, fallback to Helvetica if not available
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        # Try to register Calibri font from Windows fonts
        pdfmetrics.registerFont(TTFont("Calibri", "C:/Windows/Fonts/calibri.ttf"))
        pdfmetrics.registerFont(TTFont("Calibri-Bold", "C:/Windows/Fonts/calibrib.ttf"))
        font_name = "Calibri"
        font_name_bold = "Calibri-Bold"
    except:
        # Fallback to Helvetica if Calibri is not available
        font_name = "Helvetica"
        font_name_bold = "Helvetica-Bold"

    # Title
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=14,
        textColor=colors.HexColor("#000000"),
        spaceAfter=2,
        alignment=1,  # TA_CENTER = 1
        fontName=font_name_bold,
    )
    story.append(Paragraph(title, title_style))

    # Subtitle
    if subtitle:
        subtitle_style = ParagraphStyle(
            "CustomSubtitle",
            parent=styles["Normal"],
            fontSize=14,
            textColor=colors.HexColor("#000000"),
            spaceBefore=0,
            spaceAfter=10,
            alignment=1,  # TA_CENTER = 1
            fontName=font_name_bold,
        )
        story.append(Paragraph(subtitle, subtitle_style))

    # Select relevant columns for display
    preferred_columns = [
        "EmployeeName",
        "DepartmentName",
        "AttendanceDate",
        "ActualCheckIn",
        "ActualCheckOut",
        "DayOff",
    ]
    display_columns = []

    # Use preferred columns if they exist
    for col in preferred_columns:
        if col in df.columns:
            display_columns.append(col)

    # If no preferred columns found, use first 6 columns
    if not display_columns:
        display_columns = list(df.columns)[:6]

    # Create cell styles for wrapped text
    cell_style = ParagraphStyle(
        "CellStyle",
        parent=styles["Normal"],
        fontSize=12,
        fontName=font_name,
        alignment=TA_CENTER,
        leading=14,
        wordWrap="CJK",
    )

    cell_style_bold = ParagraphStyle(
        "CellStyleBold",
        parent=styles["Normal"],
        fontSize=12,
        fontName=font_name_bold,
        alignment=TA_CENTER,
        leading=14,
        wordWrap="CJK",
    )

    # Prepare table data with Paragraph-wrapped headers
    table_data = []
    header_row = []
    for col in display_columns:
        header_row.append(Paragraph(str(col), cell_style_bold))
    table_data.append(header_row)

    # Data rows with color coding
    header_colors = []

    for idx, row in df.iterrows():
        row_data = []
        row_colors = []

        for col in display_columns:
            value = str(row[col]) if pd.notna(row[col]) else ""

            # Color coding logic
            cell_color = colors.white
            text_color = colors.black

            if col == "ActualCheckIn":
                # Check for absenteeism (empty check-in)
                if pd.isna(row[col]) or str(row[col]).strip() == "":
                    cell_color = colors.HexColor("#FFFF00")  # Yellow for absent
                else:
                    # Check for late comers - compare with 08:34
                    try:
                        check_in_time = str(row[col]).strip()
                        if ":" in check_in_time:
                            # Parse time (handles both HH:MM:SS and HH:MM formats)
                            time_parts = check_in_time.split(":")
                            hour = int(time_parts[0])
                            minute = int(time_parts[1]) if len(time_parts) > 1 else 0

                            # Convert to total minutes for comparison
                            check_in_minutes = hour * 60 + minute
                            late_threshold_minutes = 8 * 60 + 34  # 08:34

                            if check_in_minutes >= late_threshold_minutes:
                                text_color = colors.HexColor(
                                    "#FF0000"
                                )  # Red text for late
                    except:
                        pass

            row_colors.append((cell_color, text_color))

            # Create custom paragraph style for this cell with proper color
            cell_custom_style = ParagraphStyle(
                f"CellStyle_{idx}_{col}",
                parent=styles["Normal"],
                fontSize=12,
                fontName=font_name_bold if text_color != colors.black else font_name,
                alignment=TA_CENTER,
                textColor=text_color,
                leading=14,
                wordWrap="CJK",
            )

            # Wrap value in Paragraph for automatic text wrapping
            row_data.append(Paragraph(value, cell_custom_style))

        table_data.append(row_data)
        header_colors.append(row_colors)

    # Ensure table has data
    if len(table_data) <= 1:
        raise ValueError("Excel file has no data rows")

    # Create table with better column widths - make DepartmentName dynamic
    col_widths = []
    for col in display_columns:
        if col == "EmployeeName":
            col_widths.append(1.8 * inch)
        elif col == "DepartmentName":
            # Calculate max length for department names to fit content
            max_dept_length = max(
                [
                    len(str(row[col])) if pd.notna(row[col]) else 0
                    for _, row in df.iterrows()
                ]
                + [len(col)]
            )
            # Fixed width for department to ensure single line
            col_widths.append(2.2 * inch)
        elif col == "AttendanceDate":
            col_widths.append(1.15 * inch)
        elif col == "ActualCheckIn":
            col_widths.append(1.15 * inch)
        elif col == "ActualCheckOut":
            col_widths.append(1.15 * inch)
        else:
            col_widths.append(0.85 * inch)

    table = Table(table_data, colWidths=col_widths)

    # Apply table styling with Calibri font and size 12
    table_style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#CCCCCC")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BOX", (0, 0), (-1, -1), 1.5, colors.black),
        (
            "ROWBACKGROUNDS",
            (0, 1),
            (-1, -1),
            [colors.white, colors.HexColor("#FAFAFA")],
        ),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 1), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
    ]

    # Apply cell-specific colors for check-in column
    check_in_col = (
        display_columns.index("ActualCheckIn")
        if "ActualCheckIn" in display_columns
        else -1
    )
    if check_in_col >= 0:
        for row_idx, row_colors in enumerate(header_colors, start=1):
            cell_bg_color, text_color = row_colors[check_in_col]

            # Apply background color (yellow for absent)
            if cell_bg_color != colors.white:
                table_style.append(
                    (
                        "BACKGROUND",
                        (check_in_col, row_idx),
                        (check_in_col, row_idx),
                        cell_bg_color,
                    )
                )

    table.setStyle(TableStyle(table_style))
    story.append(table)

    story.append(Spacer(1, 0.15 * inch))

    # Add legend/notes
    legend_style = ParagraphStyle(
        "Legend",
        parent=styles["Normal"],
        fontSize=12,
        textColor=colors.black,
        fontName=font_name_bold,
        spaceAfter=2,
        alignment=1,  # TA_CENTER = 1
    )

    story.append(Paragraph("NOTE:", legend_style))

    legend_table_data = [
        ["", "THE YELLOW COLOR INDICATES ABSENTEEISM"],
        ["", "THE RED COLOR INDICATES LATE COMERS"],
    ]

    legend_table = Table(legend_table_data, colWidths=[0.3 * inch, 5.0 * inch])
    legend_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#FFFF00")),
                ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#FF0000")),
                ("TEXTCOLOR", (0, 1), (0, 1), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ]
        )
    )

    story.append(legend_table)

    # Build PDF
    doc.build(story)


if __name__ == "__main__":
    # Run on all network interfaces so other computers on the network can access
    # Access via: http://YOUR_IP_ADDRESS:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
