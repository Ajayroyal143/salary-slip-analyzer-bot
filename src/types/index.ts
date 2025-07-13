export interface SalarySlip {
    employeeId: string;
    employeeName: string;
    month: string;
    year: number;
    basicSalary: number;
    allowances: number;
    deductions: number;
    netSalary: number;
}

export interface Report {
    employeeId: string;
    employeeName: string;
    month: string;
    year: number;
    totalEarnings: number;
    totalDeductions: number;
    netSalary: number;
}