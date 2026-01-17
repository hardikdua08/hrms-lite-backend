from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# =========================
# EMPLOYEE SCHEMAS
# =========================

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: str
    joining_date: Optional[date] = None
    status: Optional[str] = "active"


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        orm_mode = True


# =========================
# ATTENDANCE SCHEMAS
# =========================

class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    status: str  # Present / Absent


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceResponse(AttendanceBase):
    id: int

    class Config:
        orm_mode = True
