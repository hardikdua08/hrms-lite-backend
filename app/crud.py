from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas


# =========================
# EMPLOYEE CRUD
# =========================

def get_employees(db: Session):
    return db.query(models.Employee).all()


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    # Duplicate email check
    existing = (
        db.query(models.Employee)
        .filter(models.Employee.email == employee.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this email already exists"
        )

    new_employee = models.Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        joining_date=employee.joining_date,
        status=employee.status
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


def delete_employee(db: Session, employee_id: int):
    employee = (
        db.query(models.Employee)
        .filter(models.Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}


# =========================
# ATTENDANCE
# =========================

def mark_attendance(db: Session, attendance: schemas.AttendanceCreate):
    employee = (
        db.query(models.Employee)
        .filter(models.Employee.id == attendance.employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    # Prevent duplicate attendance for same date
    existing_attendance = (
        db.query(models.Attendance)
        .filter(
            models.Attendance.employee_id == attendance.employee_id,
            models.Attendance.date == attendance.date
        )
        .first()
    )

    if existing_attendance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already marked for this date"
        )

    record = models.Attendance(
        employee_id=attendance.employee_id,
        date=attendance.date,
        status=attendance.status
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_attendance_by_employee(db: Session, employee_id: int):
    return (
        db.query(models.Attendance)
        .filter(models.Attendance.employee_id == employee_id)
        .all()
    )
