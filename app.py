import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pdfplumber
import re

# ------------------------ Parser Function ------------------------
def parse_salary_slip(text):
    patterns = {
        'Employee Name': r'Employee Name:\s*(.*)',
        'Employee ID': r'Employee ID:\s*(.*)',
        'Designation': r'Designation:\s*(.*)',
        'Department': r'Department:\s*(.*)',
        'Pay Period': r'Pay Period:\s*(.*)',
        'Basic Pay': r'Basic Pay:\s*INR\s*([\d,]+)',
        'HRA': r'HRA:\s*INR\s*([\d,]+)',
        'Conveyance': r'Conveyance:\s*INR\s*([\d,]+)',
        'Special Allowance': r'Special Allowance:\s*INR\s*([\d,]+)',
        'PF': r'PF:\s*INR\s*([\d,]+)',
        'Professional Tax': r'Professional Tax:\s*INR\s*([\d,]+)',
        'TDS': r'TDS:\s*INR\s*([\d,]+)',
        'Net Pay': r'Net Pay:\s*INR\s*([\d,]+)',
    }

    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            extracted[key] = match.group(1).replace(',', '')
        else:
            extracted[key] = None
    return extracted

# ------------------------ PDF/Text Reader ------------------------
def read_text(file):
    if file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    else:
        return file.read().decode("utf-8")

# ------------------------ Visualization ------------------------
def plot_salary_breakdown(data):
    earnings_keys = ['Basic Pay', 'HRA', 'Conveyance', 'Special Allowance']
    deductions_keys = ['PF', 'Professional Tax', 'TDS']

    earnings = {k: float(data[k]) for k in earnings_keys if data[k]}
    deductions = {k: float(data[k]) for k in deductions_keys if data[k]}

    st.subheader("📊 Earnings vs Deductions")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Earnings")
        st.bar_chart(pd.Series(earnings))

    with col2:
        st.write("### Deductions")
        st.bar_chart(pd.Series(deductions))

# ------------------------ Streamlit UI ------------------------
st.set_page_config(page_title="Salary Slip Analyzer", page_icon="🧾")
st.title("🧾 Salary Slip Analyzer Bot")
st.markdown("Upload a `.pdf` or `.txt` salary slip and extract structured insights.")

uploaded_file = st.file_uploader("Upload Salary Slip", type=["pdf", "txt"])

if uploaded_file:
    raw_text = read_text(uploaded_file)
    extracted = parse_salary_slip(raw_text)

    st.success("✅ Extracted Details:")
    df = pd.DataFrame([extracted])
    st.dataframe(df)

    if extracted.get("Net Pay"):
        plot_salary_breakdown(extracted)

    st.download_button("📥 Download Extracted Data as CSV",
                       df.to_csv(index=False),
                       file_name="extracted_salary.csv")
