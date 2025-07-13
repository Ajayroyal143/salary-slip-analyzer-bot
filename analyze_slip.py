import pdfplumber

def read_text_from_pdf(pdf_path):
    """Extract raw text from a PDF file using pdfplumber"""
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

import pandas as pd
from pathlib import Path
from utils.parser import parse_salary_slip

def main():
    # Load either a text or PDF salary slip
    pdf_path = Path("samples/sample_salary_slip.pdf")
    txt_path = Path("samples/sample_salary_slip.txt")

    if pdf_path.exists():
        print(f"📄 Reading from PDF: {pdf_path.name}")
        slip_text = read_text_from_pdf(pdf_path)
    elif txt_path.exists():
        print(f"📄 Reading from TXT: {txt_path.name}")
        slip_text = txt_path.read_text(encoding="utf-8")
    else:
        print("❌ No salary slip file found in samples/. Please add a .txt or .pdf file.")
        return

    # Extract data
    extracted_data = parse_salary_slip(slip_text)

    # Convert to DataFrame
    df = pd.DataFrame([extracted_data])
    print("✅ Extracted Data:")
    print(df)

    # Ensure output directory exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Save as CSV
    df.to_csv(output_dir / "extracted_salary.csv", index=False)
    print("\n✅ Saved to output/extracted_salary.csv")

    # Step 4: Visualize earnings vs deductions
    import matplotlib.pyplot as plt

    def plot_salary_breakdown(data):
        earnings_keys = ['Basic Pay', 'HRA', 'Conveyance', 'Special Allowance']
        deductions_keys = ['PF', 'Professional Tax', 'TDS']

        earnings = {k: float(data[k]) for k in earnings_keys if data[k]}
        deductions = {k: float(data[k]) for k in deductions_keys if data[k]}

        # Plot
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))
        
        axs[0].bar(earnings.keys(), earnings.values(), color='green')
        axs[0].set_title("Earnings Breakdown")
        axs[0].set_ylabel("Amount (INR)")

        axs[1].bar(deductions.keys(), deductions.values(), color='red')
        axs[1].set_title("Deductions Breakdown")
        axs[1].set_ylabel("Amount (INR)")

        plt.tight_layout()
        plt.show()

    # Call the plotting function
    plot_salary_breakdown(extracted_data)

if __name__ == "__main__":
    main()