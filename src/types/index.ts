export interface Employee {
  id: string;
  employee_id: string;
  full_name: string;
  email: string;
  department: string;
  created_at: string;
  updated_at: string;
}

export interface Attendance {
  id: string;
  employee_id: string;
  attendance_date: string;
  status: 'Present' | 'Absent';
  created_at: string;
  updated_at: string;
}

export interface EmployeeWithAttendance extends Employee {
  attendance?: Attendance[];
}
