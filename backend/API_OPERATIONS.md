# HRMS Lite Backend - Available Operations

This document describes all operations you can perform on the HRMS Lite backend API.

## Base URL
- **Development**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

---

## 🔵 Employee Operations

### 1. Get All Employees
**GET** `/api/employees`

Retrieve all employees with optional sorting.

**Query Parameters:**
- `order_by` (optional): Field to sort by
  - Options: `created_at`, `full_name`, `employee_id`
  - Default: `created_at`
- `order` (optional): Sort direction
  - Options: `asc`, `desc`
  - Default: `desc`

**Example Requests:**
```bash
# Get all employees (default: newest first)
curl http://localhost:8000/api/employees

# Get all employees sorted by name (A-Z)
curl "http://localhost:8000/api/employees?order_by=full_name&order=asc"

# Get all employees sorted by employee_id
curl "http://localhost:8000/api/employees?order_by=employee_id&order=asc"
```

**Response:**
```json
[
  {
    "id": "uuid-string",
    "employee_id": "EMP001",
    "full_name": "John Doe",
    "email": "john.doe@company.com",
    "department": "Engineering",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 2. Get Single Employee
**GET** `/api/employees/{id}`

Retrieve a specific employee by their ID.

**Path Parameters:**
- `id` (required): Employee UUID

**Example Request:**
```bash
curl http://localhost:8000/api/employees/123e4567-e89b-12d3-a456-426614174000
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "employee_id": "EMP001",
  "full_name": "John Doe",
  "email": "john.doe@company.com",
  "department": "Engineering",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `404 Not Found`: Employee doesn't exist

---

### 3. Create Employee
**POST** `/api/employees`

Create a new employee record.

**Request Body:**
```json
{
  "employee_id": "EMP001",
  "full_name": "John Doe",
  "email": "john.doe@company.com",
  "department": "Engineering"
}
```

**Example Request:**
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

**Response:** `201 Created`
```json
{
  "id": "uuid-generated",
  "employee_id": "EMP001",
  "full_name": "John Doe",
  "email": "john.doe@company.com",
  "department": "Engineering",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Validation Rules:**
- `employee_id`: Required, must be unique
- `full_name`: Required, minimum 1 character
- `email`: Required, must be valid email format, must be unique
- `department`: Required, minimum 1 character

**Error Responses:**
- `400 Bad Request`: 
  - Employee ID already exists
  - Email already exists
  - Invalid email format
  - Missing required fields

---

### 4. Delete Employee
**DELETE** `/api/employees/{id}`

Delete an employee and all their attendance records (cascade delete).

**Path Parameters:**
- `id` (required): Employee UUID

**Example Request:**
```bash
curl -X DELETE "http://localhost:8000/api/employees/123e4567-e89b-12d3-a456-426614174000"
```

**Response:** `204 No Content` (empty body)

**Error Responses:**
- `404 Not Found`: Employee doesn't exist
- `500 Internal Server Error`: Database error

**Note:** This operation will also delete all attendance records associated with the employee.

---

## 📅 Attendance Operations

### 1. Get Attendance Records
**GET** `/api/attendance`

Retrieve attendance records with optional filters.

**Query Parameters:**
- `attendance_date` (optional): Filter by specific date (YYYY-MM-DD)
- `employee_id` (optional): Filter by employee UUID

**Example Requests:**
```bash
# Get all attendance records
curl http://localhost:8000/api/attendance

# Get attendance for a specific date
curl "http://localhost:8000/api/attendance?attendance_date=2024-01-15"

# Get attendance for a specific employee
curl "http://localhost:8000/api/attendance?employee_id=123e4567-e89b-12d3-a456-426614174000"

# Get attendance for employee on specific date
curl "http://localhost:8000/api/attendance?attendance_date=2024-01-15&employee_id=123e4567-e89b-12d3-a456-426614174000"
```

**Response:**
```json
[
  {
    "id": "uuid-string",
    "employee_id": "employee-uuid",
    "attendance_date": "2024-01-15",
    "status": "Present",
    "created_at": "2024-01-15T08:00:00Z",
    "updated_at": "2024-01-15T08:00:00Z"
  }
]
```

---

### 2. Get Employees with Attendance
**GET** `/api/attendance/employees-with-attendance`

Get all employees with their attendance status for a specific date. This is optimized for the attendance management page.

**Query Parameters:**
- `attendance_date` (required): Date to get attendance for (YYYY-MM-DD)

**Example Request:**
```bash
curl "http://localhost:8000/api/attendance/employees-with-attendance?attendance_date=2024-01-15"
```

**Response:**
```json
[
  {
    "id": "employee-uuid-1",
    "employee_id": "EMP001",
    "full_name": "John Doe",
    "email": "john.doe@company.com",
    "department": "Engineering",
    "created_at": "2024-01-10T10:30:00Z",
    "updated_at": "2024-01-10T10:30:00Z",
    "attendance": [
      {
        "id": "attendance-uuid",
        "employee_id": "employee-uuid-1",
        "attendance_date": "2024-01-15",
        "status": "Present",
        "created_at": "2024-01-15T08:00:00Z",
        "updated_at": "2024-01-15T08:00:00Z"
      }
    ]
  },
  {
    "id": "employee-uuid-2",
    "employee_id": "EMP002",
    "full_name": "Jane Smith",
    "email": "jane.smith@company.com",
    "department": "Marketing",
    "created_at": "2024-01-10T10:30:00Z",
    "updated_at": "2024-01-10T10:30:00Z",
    "attendance": []
  }
]
```

**Note:** Employees without attendance for the date will have an empty `attendance` array.

---

### 3. Create/Update Single Attendance Record
**POST** `/api/attendance`

Create a new attendance record or update an existing one (upsert).

**Request Body:**
```json
{
  "employee_id": "employee-uuid",
  "attendance_date": "2024-01-15",
  "status": "Present"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/attendance" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "123e4567-e89b-12d3-a456-426614174000",
    "attendance_date": "2024-01-15",
    "status": "Present"
  }'
```

**Response:** `201 Created`
```json
[
  {
    "id": "uuid-generated",
    "employee_id": "123e4567-e89b-12d3-a456-426614174000",
    "attendance_date": "2024-01-15",
    "status": "Present",
    "created_at": "2024-01-15T08:00:00Z",
    "updated_at": "2024-01-15T08:00:00Z"
  }
]
```

**Validation Rules:**
- `employee_id`: Required, must exist in employees table
- `attendance_date`: Required, format: YYYY-MM-DD
- `status`: Required, must be either `"Present"` or `"Absent"`

**Behavior:**
- If attendance record exists for employee + date: **Updates** the status
- If attendance record doesn't exist: **Creates** a new record

**Error Responses:**
- `404 Not Found`: Employee doesn't exist
- `400 Bad Request`: Invalid status value or date format

---

### 4. Bulk Create/Update Attendance (Upsert)
**POST** `/api/attendance/bulk`

Create or update multiple attendance records at once. This is ideal for marking attendance for multiple employees on the same date.

**Request Body:**
```json
{
  "records": [
    {
      "employee_id": "employee-uuid-1",
      "attendance_date": "2024-01-15",
      "status": "Present"
    },
    {
      "employee_id": "employee-uuid-2",
      "attendance_date": "2024-01-15",
      "status": "Absent"
    },
    {
      "employee_id": "employee-uuid-3",
      "attendance_date": "2024-01-15",
      "status": "Present"
    }
  ]
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/attendance/bulk" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {
        "employee_id": "123e4567-e89b-12d3-a456-426614174000",
        "attendance_date": "2024-01-15",
        "status": "Present"
      },
      {
        "employee_id": "223e4567-e89b-12d3-a456-426614174001",
        "attendance_date": "2024-01-15",
        "status": "Absent"
      }
    ]
  }'
```

**Response:** `201 Created`
```json
[
  {
    "id": "uuid-1",
    "employee_id": "123e4567-e89b-12d3-a456-426614174000",
    "attendance_date": "2024-01-15",
    "status": "Present",
    "created_at": "2024-01-15T08:00:00Z",
    "updated_at": "2024-01-15T08:00:00Z"
  },
  {
    "id": "uuid-2",
    "employee_id": "223e4567-e89b-12d3-a456-426614174001",
    "attendance_date": "2024-01-15",
    "status": "Absent",
    "created_at": "2024-01-15T08:00:00Z",
    "updated_at": "2024-01-15T08:00:00Z"
  }
]
```

**Behavior:**
- For each record: If exists → **Updates**, If not → **Creates**
- Invalid employee IDs are silently skipped
- Returns only successfully processed records

**Error Responses:**
- `400 Bad Request`: Empty records array or invalid data format

---

## 🔍 System Operations

### 1. Health Check
**GET** `/health`

Check if the API is running.

**Example Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

### 2. API Information
**GET** `/`

Get basic API information.

**Example Request:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "message": "HRMS Lite API",
  "version": "1.0.0"
}
```

---

## 📊 Summary of Operations

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| **List Employees** | GET | `/api/employees` | Get all employees (with sorting) |
| **Get Employee** | GET | `/api/employees/{id}` | Get single employee |
| **Create Employee** | POST | `/api/employees` | Add new employee |
| **Delete Employee** | DELETE | `/api/employees/{id}` | Remove employee |
| **List Attendance** | GET | `/api/attendance` | Get attendance records (with filters) |
| **Get Employees with Attendance** | GET | `/api/attendance/employees-with-attendance` | Get all employees with attendance for date |
| **Mark Single Attendance** | POST | `/api/attendance` | Create/update single attendance |
| **Bulk Mark Attendance** | POST | `/api/attendance/bulk` | Create/update multiple attendance records |
| **Health Check** | GET | `/health` | Check API status |
| **API Info** | GET | `/` | Get API information |

---

## 🧪 Testing with cURL

### Complete Workflow Example

```bash
# 1. Create an employee
curl -X POST "http://localhost:8000/api/employees" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP001",
    "full_name": "John Doe",
    "email": "john.doe@company.com",
    "department": "Engineering"
  }'

# 2. Get all employees
curl http://localhost:8000/api/employees

# 3. Mark attendance for the employee
curl -X POST "http://localhost:8000/api/attendance" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMPLOYEE_UUID_FROM_STEP_1",
    "attendance_date": "2024-01-15",
    "status": "Present"
  }'

# 4. Get employees with attendance for a date
curl "http://localhost:8000/api/attendance/employees-with-attendance?attendance_date=2024-01-15"

# 5. Delete employee (also deletes attendance)
curl -X DELETE "http://localhost:8000/api/employees/EMPLOYEE_UUID"
```

---

## 📝 Notes

1. **Date Format**: All dates must be in `YYYY-MM-DD` format
2. **UUIDs**: Employee and Attendance IDs are UUIDs (strings)
3. **Cascade Delete**: Deleting an employee automatically deletes all their attendance records
4. **Unique Constraints**: 
   - Employee `employee_id` must be unique
   - Employee `email` must be unique
   - One attendance record per employee per date
5. **Upsert Behavior**: Creating attendance for an existing employee+date combination updates the record
6. **CORS**: API accepts requests from `localhost:5173`, `localhost:3000`, and `127.0.0.1:5173`

---

## 🔗 Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI where you can:
- See all endpoints
- Test API calls directly in the browser
- View request/response schemas
- See example requests and responses

