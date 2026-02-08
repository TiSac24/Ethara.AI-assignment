/*
  # Create HRMS Lite Database Schema

  1. New Tables
    - `employees`
      - `id` (uuid, primary key) - Internal unique identifier
      - `employee_id` (text, unique) - User-facing Employee ID
      - `full_name` (text) - Employee's full name
      - `email` (text, unique) - Employee's email address
      - `department` (text) - Department name
      - `created_at` (timestamptz) - Record creation timestamp
      - `updated_at` (timestamptz) - Record update timestamp
    
    - `attendance`
      - `id` (uuid, primary key) - Unique identifier for attendance record
      - `employee_id` (uuid, foreign key) - References employees table
      - `attendance_date` (date) - Date of attendance
      - `status` (text) - Present or Absent
      - `created_at` (timestamptz) - Record creation timestamp
      - `updated_at` (timestamptz) - Record update timestamp
  
  2. Security
    - Enable RLS on both tables
    - Add policies for public access (since no authentication is required per spec)
  
  3. Important Notes
    - Employee ID is unique and user-defined
    - Email must be unique
    - Attendance records are linked to employees via foreign key
    - Constraint ensures one attendance record per employee per day
*/

CREATE TABLE IF NOT EXISTS employees (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  employee_id text UNIQUE NOT NULL,
  full_name text NOT NULL,
  email text UNIQUE NOT NULL,
  department text NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS attendance (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  employee_id uuid NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
  attendance_date date NOT NULL,
  status text NOT NULL CHECK (status IN ('Present', 'Absent')),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(employee_id, attendance_date)
);

CREATE INDEX IF NOT EXISTS idx_attendance_employee ON attendance(employee_id);
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(attendance_date);

ALTER TABLE employees ENABLE ROW LEVEL SECURITY;
ALTER TABLE attendance ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access to employees"
  ON employees FOR SELECT
  TO anon
  USING (true);

CREATE POLICY "Allow public insert to employees"
  ON employees FOR INSERT
  TO anon
  WITH CHECK (true);

CREATE POLICY "Allow public update to employees"
  ON employees FOR UPDATE
  TO anon
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow public delete from employees"
  ON employees FOR DELETE
  TO anon
  USING (true);

CREATE POLICY "Allow public read access to attendance"
  ON attendance FOR SELECT
  TO anon
  USING (true);

CREATE POLICY "Allow public insert to attendance"
  ON attendance FOR INSERT
  TO anon
  WITH CHECK (true);

CREATE POLICY "Allow public update to attendance"
  ON attendance FOR UPDATE
  TO anon
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow public delete from attendance"
  ON attendance FOR DELETE
  TO anon
  USING (true);