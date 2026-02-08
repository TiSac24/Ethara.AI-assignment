from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date, datetime


# Employee Schemas
class EmployeeBase(BaseModel):
    employee_id: str = Field(..., min_length=1, description="Unique employee identifier")
    full_name: str = Field(..., min_length=1, description="Employee's full name")
    email: EmailStr
    department: str = Field(..., min_length=1, description="Department name")


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    employee_id: Optional[str] = Field(None, min_length=1)
    full_name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(None, min_length=1)


class EmployeeResponse(EmployeeBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Attendance Schemas
class AttendanceBase(BaseModel):
    employee_id: str
    attendance_date: date
    status: str = Field(..., description="Must be 'Present' or 'Absent'")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v not in ['Present', 'Absent']:
            raise ValueError("Status must be 'Present' or 'Absent'")
        return v


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceBulkCreate(BaseModel):
    records: list[AttendanceCreate]


class AttendanceResponse(AttendanceBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmployeeWithAttendance(EmployeeResponse):
    attendance: list[AttendanceResponse] = []

