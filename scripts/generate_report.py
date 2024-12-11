import os
from fpdf import FPDF
import pandas as pd

# Define input and output paths relative to the script's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of the current script
INPUT_CSV_PATH = os.path.join(BASE_DIR, "..", "data", "tenders.csv")
OUTPUT_PDF_PATH = os.path.join(BASE_DIR, "..", "data", "tender_analysis_report.pdf")
FONT_PATH = os.path.join(BASE_DIR, "..", "fonts", "DejaVuSans.ttf")  # Path to the font


# Function to generate PDF report
def generate_pdf_report():
    # Check if the required files exist
    if not os.path.exists(INPUT_CSV_PATH):
        raise FileNotFoundError(f"CSV file not found at: {INPUT_CSV_PATH}")
    if not os.path.exists(FONT_PATH):
        raise FileNotFoundError(f"Font file not found at: {FONT_PATH}")

    # Load data
    df = pd.read_csv(INPUT_CSV_PATH)

    # Prepare analysis
    total_tenders = len(df)
    top_organization = df['organization'].value_counts().idxmax()
    top_organization_count = df['organization'].value_counts().max()
    publish_dates = pd.to_datetime(df['publish_date'])
    first_date = publish_dates.min()
    last_date = publish_dates.max()

    # Initialize PDF
    pdf = FPDF()
    pdf.add_page()

    # Add custom font
    pdf.add_font('DejaVu', '', FONT_PATH, uni = True)  # Register the regular font
    pdf.set_font("DejaVu", size = 16)  # Use the registered font without style

    # Title
    pdf.cell(200, 10, txt = "Tender Analysis Report", ln = True, align = 'C')

    # Summary Section
    pdf.set_font("DejaVu", size = 12)  # Use the registered font for body text
    pdf.cell(200, 10, txt = f"Total tenders: {total_tenders}", ln = True)
    pdf.cell(200, 10, txt = f"Top organization: {top_organization} with {top_organization_count} tenders", ln = True)
    pdf.cell(200, 10, txt = f"Date range: {first_date.date()} to {last_date.date()}", ln = True)

    # Detailed Analysis Section
    pdf.set_font("DejaVu", size = 14)  # Slightly larger font for section headers
    pdf.cell(200, 10, txt = "\nNumber of tenders by top 10 organizations:", ln = True)

    pdf.set_font("DejaVu", size = 12)  # Back to regular size
    org_counts = df['organization'].value_counts().head(10)
    for org, count in org_counts.items():
        pdf.cell(200, 10, txt = f"{org}: {count} tenders", ln = True)

    # Save PDF
    pdf.output(OUTPUT_PDF_PATH)
    print(f"PDF report generated successfully: {OUTPUT_PDF_PATH}")


# Run the function
if __name__ == "__main__":
    generate_pdf_report()
