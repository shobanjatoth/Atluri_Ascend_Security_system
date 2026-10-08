from datetime import datetime, date

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Index,
)

from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.connection import Base


# ============================================================
# USER MODEL
# ============================================================

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="EMPLOYEE"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationship
    employee = relationship(
        "Employee",
        back_populates="user",
        uselist=False
    )

    audit_logs = relationship(
        "AuditLog",
        back_populates="user"
    )


# ============================================================
# DEPARTMENT MODEL
# ============================================================

class Department(Base):

    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationship
    employees = relationship(
        "Employee",
        back_populates="department"
    )


# ============================================================
# EMPLOYEE MODEL
# ============================================================

class Employee(Base):

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    department_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("departments.id"),
        nullable=True
    )

    designation: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    joining_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="ACTIVE",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships

    user = relationship(
        "User",
        back_populates="employee"
    )

    department = relationship(
        "Department",
        back_populates="employees"
    )

    attendance_records = relationship(
        "Attendance",
        back_populates="employee"
    )


# ============================================================
# QR SESSION MODEL
# ============================================================

class QRSession(Base):

    __tablename__ = "qr_sessions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    token_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        index=True
    )

    location: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    # Relationships

    check_in_records = relationship(
        "Attendance",
        foreign_keys="Attendance.check_in_qr_id",
        back_populates="check_in_qr"
    )

    check_out_records = relationship(
        "Attendance",
        foreign_keys="Attendance.check_out_qr_id",
        back_populates="check_out_qr"
    )


# ============================================================
# ATTENDANCE MODEL
# ============================================================

class Attendance(Base):

    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
        index=True
    )

    attendance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True
    )

    check_in: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    check_out: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    working_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    status: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    is_late: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    check_in_qr_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("qr_sessions.id"),
        nullable=True
    )

    check_out_qr_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("qr_sessions.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships

    employee = relationship(
        "Employee",
        back_populates="attendance_records"
    )

    check_in_qr = relationship(
        "QRSession",
        foreign_keys=[check_in_qr_id],
        back_populates="check_in_records"
    )

    check_out_qr = relationship(
        "QRSession",
        foreign_keys=[check_out_qr_id],
        back_populates="check_out_records"
    )

    # Prevent multiple attendance records
    # for the same employee on the same day.
    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "attendance_date",
            name="uq_employee_attendance_date"
        ),
        Index(
            "ix_attendance_employee_date",
            "employee_id",
            "attendance_date"
        ),
    )


# ============================================================
# AUDIT LOG MODEL
# ============================================================

class AuditLog(Base):

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    device_info: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    # Relationship

    user = relationship(
        "User",
        back_populates="audit_logs"
    )