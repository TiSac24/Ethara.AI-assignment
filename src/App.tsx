import { useState } from 'react';
import { Users, Calendar } from 'lucide-react';
import EmployeeManagement from './components/EmployeeManagement';
import AttendanceManagement from './components/AttendanceManagement';

type Tab = 'employees' | 'attendance';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('employees');

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <Users className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">HRMS Lite</h1>
                <p className="text-xs text-gray-500">Human Resource Management System</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('employees')}
              className={`flex items-center space-x-2 px-1 py-4 border-b-2 text-sm font-medium transition-colors ${
                activeTab === 'employees'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Users className="w-4 h-4" />
              <span>Employee Management</span>
            </button>
            <button
              onClick={() => setActiveTab('attendance')}
              className={`flex items-center space-x-2 px-1 py-4 border-b-2 text-sm font-medium transition-colors ${
                activeTab === 'attendance'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Calendar className="w-4 h-4" />
              <span>Attendance Management</span>
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'employees' ? <EmployeeManagement /> : <AttendanceManagement />}
      </main>
    </div>
  );
}

export default App;
