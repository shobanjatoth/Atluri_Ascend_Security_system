# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.core.dependencies import require_admin
# from app.database.connection import get_db
# from app.database.models import User
# from app.schemas.report import AttendanceReportResponse
# from app.services.report_service import get_attendance_report


# router = APIRouter(
#     prefix="/api/reports",
#     tags=["Reports"],
# )


# @router.get(
#     "/attendance",
#     response_model=AttendanceReportResponse,
# )
# def attendance_report(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin),
# ):
#     return get_attendance_report(db)



from fastapi.responses import Response, StreamingResponse
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.database.connection import get_db
from app.database.models import User
from app.schemas.report import AttendanceReportResponse

from app.services.report_service import (
    create_csv_report,
    create_excel_report,
    get_attendance_report,
)

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
)


@router.get(
    "/attendance",
    response_model=AttendanceReportResponse,
)
def attendance_report(
    start_date: date | None = Query(
        default=None,
        description="Report start date",
    ),
    end_date: date | None = Query(
        default=None,
        description="Report end date",
    ),
    employee_id: int | None = Query(
        default=None,
        description="Filter by employee ID",
    ),
    department_id: int | None = Query(
        default=None,
        description="Filter by department ID",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_attendance_report(
        db=db,
        start_date=start_date,
        end_date=end_date,
        employee_id=employee_id,
        department_id=department_id,
    )
    
    

@router.get("/attendance/csv")
def export_attendance_csv(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    employee_id: int | None = Query(default=None),
    department_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    report = get_attendance_report(
        db=db,
        start_date=start_date,
        end_date=end_date,
        employee_id=employee_id,
        department_id=department_id,
    )

    csv_content = create_csv_report(report["records"])

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                "attachment; filename=attendance_report.csv"
            )
        },
    )


@router.get("/attendance/excel")
def export_attendance_excel(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    employee_id: int | None = Query(default=None),
    department_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    report = get_attendance_report(
        db=db,
        start_date=start_date,
        end_date=end_date,
        employee_id=employee_id,
        department_id=department_id,
    )

    excel_file = create_excel_report(report["records"])

    return StreamingResponse(
        excel_file,
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition": (
                "attachment; filename=attendance_report.xlsx"
            )
        },
    )