import os
from PyPDF2 import PdfReader, PdfWriter

def crop_pdf(input_path, output_path, left_right_inch=0.01, bottom_inch=0.85):
    margin_lr = left_right_inch * 72  # 1 inch = 72 points
    margin_bottom = bottom_inch * 72

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        media_box = page.mediabox

        # Get original coordinates
        llx = float(media_box.lower_left[0]) + margin_lr
        lly = float(media_box.lower_left[1]) + margin_bottom
        urx = float(media_box.upper_right[0]) - margin_lr
        ury = float(media_box.upper_right[1])

        # Set new crop box
        page.mediabox.lower_left = (llx, lly)
        page.mediabox.upper_right = (urx, ury)

        writer.add_page(page)

    with open(output_path, "wb") as f_out:
        writer.write(f_out)

    print(f"Cropped PDF saved as: {output_path}")

# === Example Usage ===
input_pdf = ".pdf"     # Replace with your input PDF file path
output_pdf = ".pdf"  # Output path
crop_pdf(input_pdf, output_pdf)
