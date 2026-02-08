import { useState, useEffect } from 'react';
import { X, AlertCircle, Loader2, CheckCircle, XCircle } from 'lucide-react';
import { supabase } from '../lib/supabase';
import type { Employee, Attendance } from '../types';

interface EmployeeWithAttendance extends Employee {
  attendance: Attendance[];
}

interface MarkAttendanceModalProps {
  employees: EmployeeWithAttendance[];
  selectedDate: string;
  onClose: () => void;
  onSuccess: () => void;
}

export default function MarkAttendanceModal({
  employees,
  selectedDate,
  onClose,
  onSuccess
}: MarkAttendanceModalProps) {
  const [attendanceData, setAttendanceData] = useState<Record<string, 'Present' | 'Absent' | null>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initialData: Record<string, 'Present' | 'Absent' | null> = {};
    employees.forEach(emp => {
      const existingAttendance = emp.attendance.find(att => att.attendance_date === selectedDate);
      initialData[emp.id] = existingAttendance?.status || null;
    });
    setAttendanceData(initialData);
  }, [employees, selectedDate]);

  const handleStatusChange = (employeeId: string, status: 'Present' | 'Absent' | null) => {
    setAttendanceData(prev => ({
      ...prev,
      [employeeId]: status,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const recordsToUpsert = Object.entries(attendanceData)
      .filter(([_, status]) => status !== null)
      .map(([employeeId, status]) => ({
        employee_id: employeeId,
        attendance_date: selectedDate,
        status: status as 'Present' | 'Absent',
      }));

    if (recordsToUpsert.length === 0) {
      setError('Please mark attendance for at least one employee');
      return;
    }

    try {
      setLoading(true);

      const { error: upsertError } = await supabase
        .from('attendance')
        .upsert(recordsToUpsert, {
          onConflict: 'employee_id,attendance_date',
        });

      if (upsertError) throw upsertError;

      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to mark attendance');
    } finally {
      setLoading(false);
    }
  };

  const markedCount = Object.values(attendanceData).filter(status => status !== null).length;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] flex flex-col">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Mark Attendance</h3>
            <p className="text-sm text-gray-600 mt-1">
              Date: {new Date(selectedDate).toLocaleDateString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
            disabled={loading}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex-1 flex flex-col overflow-hidden">
          <div className="flex-1 overflow-y-auto p-6">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-start space-x-2 mb-4">
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            {employees.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-gray-600">No employees found</p>
              </div>
            ) : (
              <div className="space-y-3">
                {employees.map((employee) => (
                  <div
                    key={employee.id}
                    className="bg-gray-50 rounded-lg p-4 border border-gray-200"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3">
                          <h4 className="text-sm font-medium text-gray-900">{employee.full_name}</h4>
                          <span className="text-xs text-gray-500">{employee.employee_id}</span>
                        </div>
                        <p className="text-xs text-gray-600 mt-1">{employee.department}</p>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          type="button"
                          onClick={() => handleStatusChange(employee.id, 'Present')}
                          className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
                            attendanceData[employee.id] === 'Present'
                              ? 'bg-green-100 border-green-300 text-green-800'
                              : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                          }`}
                          disabled={loading}
                        >
                          <CheckCircle className="w-4 h-4" />
                          <span className="text-sm font-medium">Present</span>
                        </button>
                        <button
                          type="button"
                          onClick={() => handleStatusChange(employee.id, 'Absent')}
                          className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
                            attendanceData[employee.id] === 'Absent'
                              ? 'bg-red-100 border-red-300 text-red-800'
                              : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                          }`}
                          disabled={loading}
                        >
                          <XCircle className="w-4 h-4" />
                          <span className="text-sm font-medium">Absent</span>
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="border-t border-gray-200 p-6 bg-gray-50">
            <div className="flex items-center justify-between mb-4">
              <p className="text-sm text-gray-600">
                Marked: <span className="font-semibold text-gray-900">{markedCount}</span> of{' '}
                <span className="font-semibold text-gray-900">{employees.length}</span> employees
              </p>
            </div>
            <div className="flex space-x-3">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-white transition-colors"
                disabled={loading}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                disabled={loading || markedCount === 0}
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Saving...</span>
                  </>
                ) : (
                  <span>Save Attendance</span>
                )}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
