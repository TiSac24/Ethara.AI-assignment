from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import date
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from database import get_db
import models
import schemas

router = APIRouter()


@router.get("/attendance", response_model=List[schemas.AttendanceResponse])
def get_attendance(
    attendance_date: Optional[date] = Query(None, description="Filter by attendance date"),
    employee_id: Optional[str] = Query(None, description="Filter by employee ID"),
    db: Session = Depends(get_db)
):
    """Get attendance records with optional filters"""
    try:
        query = db.query(models.Attendance)
        
        if attendance_date:
            query = query.filter(models.Attendance.attendance_date == attendance_date)
        
        if employee_id:
            query = query.filter(models.Attendance.employee_id == employee_id)
        
        attendance_records = query.all()
        return attendance_records
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch attendance: {str(e)}"
        )


@router.get("/attendance/employees-with-attendance", response_model=List[schemas.EmployeeWithAttendance])
def get_employees_with_attendance(
    attendance_date: date = Query(..., description="Date to get attendance for"),
    db: Session = Depends(get_db)
):
    """
    Get all employees with their attendance status for a specific date.
    This matches the frontend's requirement for the attendance management page.
    """
    try:
        # Get all employees
        employees = db.query(models.Employee).order_by(models.Employee.full_name.asc()).all()
        
        # Get attendance for the specified date
        attendance_records = db.query(models.Attendance).filter(
            models.Attendance.attendance_date == attendance_date
        ).all()
        
        # Create a map of employee_id -> attendance records
        attendance_map = {}
        for att in attendance_records:
            if att.employee_id not in attendance_map:
                attendance_map[att.employee_id] = []
            attendance_map[att.employee_id].append(att)
        
        # Combine employees with their attendance
        result = []
        for emp in employees:
            emp_dict = {
                "id": emp.id,
                "employee_id": emp.employee_id,
                "full_name": emp.full_name,
                "email": emp.email,
                "department": emp.department,
                "created_at": emp.created_at,
                "updated_at": emp.updated_at,
                "attendance": attendance_map.get(emp.id, [])
            }
            result.append(emp_dict)
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch employees with attendance: {str(e)}"
        )


@router.post("/attendance", response_model=List[schemas.AttendanceResponse], status_code=status.HTTP_201_CREATED)
def create_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    """Create a single attendance record"""
    try:
        # Verify employee exists
        employee = db.query(models.Employee).filter(models.Employee.id == attendance.employee_id).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        
        # Check if attendance already exists for this employee and date
        existing = db.query(models.Attendance).filter(
            models.Attendance.employee_id == attendance.employee_id,
            models.Attendance.attendance_date == attendance.attendance_date
        ).first()
        
        if existing:
            # Update existing record
            existing.status = attendance.status
            db.commit()
            db.refresh(existing)
            return [existing]
        else:
            # Create new record
            db_attendance = models.Attendance(
                employee_id=attendance.employee_id,
                attendance_date=attendance.attendance_date,
                status=attendance.status
            )
            db.add(db_attendance)
            db.commit()
            db.refresh(db_attendance)
            return [db_attendance]
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create attendance: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create attendance: {str(e)}"
        )


@router.post("/attendance/bulk", response_model=List[schemas.AttendanceResponse], status_code=status.HTTP_201_CREATED)
def bulk_create_attendance(attendance_data: schemas.AttendanceBulkCreate, db: Session = Depends(get_db)):
    """
    Create or update multiple attendance records (upsert).
    This matches the frontend's requirement for bulk marking attendance.
    """
    if not attendance_data.records:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No attendance records provided"
        )
    
    try:
        created_records = []
        
        for record in attendance_data.records:
            # Verify employee exists
            employee = db.query(models.Employee).filter(models.Employee.id == record.employee_id).first()
            if not employee:
                continue  # Skip invalid employee IDs
            
            # Check if attendance already exists
            existing = db.query(models.Attendance).filter(
                models.Attendance.employee_id == record.employee_id,
                models.Attendance.attendance_date == record.attendance_date
            ).first()
            
            if existing:
                # Update existing record
                existing.status = record.status
                created_records.append(existing)
            else:
                # Create new record
                db_attendance = models.Attendance(
                    employee_id=record.employee_id,
                    attendance_date=record.attendance_date,
                    status=record.status
                )
                db.add(db_attendance)
                created_records.append(db_attendance)
        
        db.commit()
        
        # Refresh all records
        for record in created_records:
            db.refresh(record)
        
        return created_records
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create attendance records: {str(e)}"
        )

