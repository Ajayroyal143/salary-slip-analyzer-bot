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
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    else:
        return file.read().decode("utf-8")

# ------------------------ Salary Charts ------------------------
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

def plot_netpay_trend(df):
    df_plot = df.dropna(subset=["Pay Period", "Net Pay"]).copy()
    df_plot["Net Pay"] = df_plot["Net Pay"].astype(float)
    df_plot["Pay Period"] = pd.to_datetime(df_plot["Pay Period"], format="%B %Y", errors="coerce")
    df_plot = df_plot.dropna(subset=["Pay Period"]).sort_values("Pay Period")

    if not df_plot.empty:
        st.subheader("📈 Net Pay Trend Over Time")
        st.line_chart(df_plot.set_index("Pay Period")["Net Pay"])

# ------------------------ Streamlit UI ------------------------
st.set_page_config(page_title="Salary Slip Analyzer", page_icon="🧾")
st.title("🧾 Salary Slip Analyzer Bot")
st.markdown("Upload one or more `.pdf` or `.txt` salary slips to analyze earnings, deductions, and trends.")

uploaded_files = st.file_uploader("Upload Salary Slips", type=["pdf", "txt"], accept_multiple_files=True)

if uploaded_files:
    all_data = []

    for file in uploaded_files:
        text = read_text(file)
        data = parse_salary_slip(text)
        data["Source File"] = file.name
        all_data.append(data)

    df = pd.DataFrame(all_data)
    st.success("✅ Extracted Salary Slip Data")
    st.dataframe(df)

    st.download_button("📥 Download CSV", df.to_csv(index=False), file_name="merged_salary_data.csv")

    # Show visualizations only if one file was uploaded
    if len(all_data) == 1:
        plot_salary_breakdown(all_data[0])
    elif len(all_data) > 1:
        plot_netpay_trend(df)
