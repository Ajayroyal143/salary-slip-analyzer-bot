import re

def parse_salary_slip(text):
    patterns = {
        'Employee Name': r'Employee Name:\s*(.*)',
        'Employee ID': r'Employee ID:\s*(.*)',
        'Designation': r'Designation:\s*(.*)',
        'Department': r'Department:\s*(.*)',
        'Pay Period': r'Pay Period:\s*(.*)',
        'Basic Pay': r'Basic Pay:\s*₹([\d,]+)',
        'HRA': r'HRA:\s*₹([\d,]+)',
        'Conveyance': r'Conveyance:\s*₹([\d,]+)',
        'Special Allowance': r'Special Allowance:\s*₹([\d,]+)',
        'PF': r'PF:\s*₹([\d,]+)',
        'Professional Tax': r'Professional Tax:\s*₹([\d,]+)',
        'TDS': r'TDS:\s*₹([\d,]+)',
        'Net Pay': r'Net Pay:\s*₹([\d,]+)',
    }

    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            extracted[key] = match.group(1).replace(',', '')
        else:
            extracted[key] = None
    return extracted