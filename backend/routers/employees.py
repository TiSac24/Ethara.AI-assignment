from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from database import get_db
import models
import schemas

router = APIRouter()


@router.get("/employees", response_model=List[schemas.EmployeeResponse])
def get_employees(
    order_by: str = "created_at",
    order: str = "desc",
    db: Session = Depends(get_db)
):
    """
    Get all employees with optional ordering.
    - order_by: Field to order by (created_at, full_name, employee_id)
    - order: asc or desc
    """
    try:
        order_column = getattr(models.Employee, order_by, models.Employee.created_at)
        if order.lower() == "asc":
            employees = db.query(models.Employee).order_by(order_column.asc()).all()
        else:
            employees = db.query(models.Employee).order_by(order_column.desc()).all()
        return employees
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch employees: {str(e)}"
        )


@router.get("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(employee_id: str, db: Session = Depends(get_db)):
    """Get a single employee by ID"""
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return employee


@router.post("/employees", response_model=schemas.EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    """Create a new employee"""
    try:
        # Check for duplicate employee_id
        existing_employee_id = db.query(models.Employee).filter(
            models.Employee.employee_id == employee.employee_id.strip()
        ).first()
        if existing_employee_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An employee with this Employee ID already exists"
            )

        # Check for duplicate email
        existing_email = db.query(models.Employee).filter(
            models.Employee.email == employee.email.lower().strip()
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An employee with this email already exists"
            )

        db_employee = models.Employee(
            employee_id=employee.employee_id.strip(),
            full_name=employee.full_name.strip(),
            email=employee.email.lower().strip(),
            department=employee.department.strip()
        )
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig)
        if "employee_id" in error_msg.lower() or "UNIQUE constraint" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An employee with this Employee ID already exists"
            )
        elif "email" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An employee with this email already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create employee"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create employee: {str(e)}"
        )


@router.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    """Delete an employee (cascades to attendance records)"""
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    try:
        db.delete(employee)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete employee: {str(e)}"
        )

