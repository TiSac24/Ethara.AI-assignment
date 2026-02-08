# HRMS Lite Backend API

A Python FastAPI backend for the HRMS Lite application.

## Features

- RESTful API for Employee Management
- RESTful API for Attendance Management
- SQLAlchemy ORM for database operations
- PostgreSQL or SQLite support
- CORS enabled for frontend integration
- Automatic API documentation (Swagger UI)

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Database

Create a `.env` file in the `backend` directory:

```env
# For SQLite (default, no setup needed)
DATABASE_URL=sqlite:///./hrms.db

# OR for PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/hrms_db
```

### 3. Initialize Database

The database tables will be created automatically when you start the server. Alternatively, you can manually initialize:

```bash
python init_db.py
```

### 4. Run the Server

From the `backend` directory:

```bash
# Option 1: Using the run script
python run.py

# Option 2: Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode (no auto-reload)
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## API Endpoints

### Employees

- `GET /api/employees` - Get all employees
  - Query params: `order_by` (created_at, full_name, employee_id), `order` (asc, desc)
- `GET /api/employees/{id}` - Get employee by ID
- `POST /api/employees` - Create new employee
- `DELETE /api/employees/{id}` - Delete employee

### Attendance

- `GET /api/attendance` - Get attendance records
  - Query params: `attendance_date`, `employee_id`
- `GET /api/attendance/employees-with-attendance` - Get employees with attendance for a date
  - Query param: `attendance_date` (required)
- `POST /api/attendance` - Create/update single attendance record
- `POST /api/attendance/bulk` - Create/update multiple attendance records (upsert)

## Example Requests

### Create Employee

```bash
curl -X POST "http://localhost:8000/api/employees" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP001",
    "full_name": "John Doe",
    "email": "john.doe@company.com",
    "department": "Engineering"
  }'
```

### Mark Attendance

```bash
curl -X POST "http://localhost:8000/api/attendance/bulk" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {
        "employee_id": "uuid-here",
        "attendance_date": "2024-01-15",
        "status": "Present"
      }
    ]
  }'
```

## Database Schema

### Employees Table
- `id` (UUID, Primary Key)
- `employee_id` (String, Unique)
- `full_name` (String)
- `email` (String, Unique)
- `department` (String)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Attendance Table
- `id` (UUID, Primary Key)
- `employee_id` (UUID, Foreign Key -> employees.id, CASCADE DELETE)
- `attendance_date` (Date)
- `status` (String: 'Present' or 'Absent')
- `created_at` (DateTime)
- `updated_at` (DateTime)
- Unique constraint on (employee_id, attendance_date)

## CORS Configuration

The API is configured to accept requests from:
- http://localhost:5173 (Vite default)
- http://localhost:3000 (React default)
- http://127.0.0.1:5173

To add more origins, edit `main.py` and update the `allow_origins` list in the CORS middleware.

