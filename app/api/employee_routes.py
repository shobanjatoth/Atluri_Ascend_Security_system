# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session

# from app.core.dependencies import require_admin
# from app.database.connection import get_db
# from app.database.models import User
# from app.schemas.employee import (
#     EmployeeCreate,
#     EmployeeUpdate,
#     EmployeeResponse
# )
# from app.services.employee_service import (
#     create_employee,
#     get_employees,
#     get_employee_by_id,
#     update_employee,
#     deactivate_employee
# )


# router = APIRouter(
#     prefix="/api/employees",
#     tags=["Employees"]
# )


# @router.post(
#     "",
#     response_model=EmployeeResponse,
#     status_code=status.HTTP_201_CREATED
# )
# def create_employee_endpoint(
#     employee_data: EmployeeCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin)
# ):
#     try:
#         employee = create_employee(
#             db=db,
#             employee_code=employee_data.employee_code.strip(),
#             name=employee_data.name.strip(),
#             email=employee_data.email.strip(),
#             phone=employee_data.phone,
#             department_id=employee_data.department_id,
#             designation=employee_data.designation,
#             joining_date=employee_data.joining_date
#         )

#         return employee

#     except ValueError as error:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail=str(error)
#         )


# @router.get(
#     "",
#     response_model=list[EmployeeResponse]
# )
# def list_employees(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin)
# ):
#     return get_employees(db)


# @router.get(
#     "/{employee_id}",
#     response_model=EmployeeResponse
# )
# def get_employee(
#     employee_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin)
# ):
#     employee = get_employee_by_id(
#         db=db,
#         employee_id=employee_id
#     )

#     if employee is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Employee not found"
#         )

#     return employee


# @router.put(
#     "/{employee_id}",
#     response_model=EmployeeResponse
# )
# def update_employee_endpoint(
#     employee_id: int,
#     employee_data: EmployeeUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin)
# ):
#     employee = get_employee_by_id(
#         db=db,
#         employee_id=employee_id
#     )

#     if employee is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Employee not found"
#         )

#     try:
#         return update_employee(
#             db=db,
#             employee=employee,
#             employee_data=employee_data
#         )

#     except ValueError as error:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail=str(error)
#         )


# @router.delete(
#     "/{employee_id}",
#     response_model=EmployeeResponse
# )
# def delete_employee(
#     employee_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin)
# ):
#     employee = get_employee_by_id(
#         db=db,
#         employee_id=employee_id
#     )

#     if employee is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Employee not found"
#         )

#     return deactivate_employee(
#         db=db,
#         employee=employee
#     )








from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import (
    get_current_user,
    require_admin,
)
# from app.core.dependencies import require_admin
from app.database.connection import get_db
from app.database.models import Employee, User
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)


from app.services.employee_service import (
    create_employee,
    deactivate_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
)


router = APIRouter(
    prefix="/api/employees",
    tags=["Employee Management"],
)


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee_route(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        employee = create_employee(
            db=db,
            employee_code=employee_data.employee_code,
            username=employee_data.username,
            password=employee_data.password,
            name=employee_data.name,
            email=employee_data.email,
            phone=employee_data.phone,
            department_id=employee_data.department_id,
            designation=employee_data.designation,
            joining_date=employee_data.joining_date,
            admin_user_id=current_user.id,
        )

        return employee

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.get(
    "",
    response_model=list[EmployeeResponse],
)
def list_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_all_employees(db=db)




@router.get(
    "/me",
    response_model=EmployeeResponse,
)
def get_my_employee_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employee = (
        db.query(Employee)
        .filter(
            Employee.user_id == current_user.id
        )
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found",
        )

    return employee








@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    employee = get_employee_by_id(
        db=db,
        employee_id=employee_id,
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return employee


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def update_employee_route(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    employee = get_employee_by_id(
        db=db,
        employee_id=employee_id,
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    try:
        employee = update_employee(
            db=db,
            employee=employee,
            name=employee_data.name,
            email=employee_data.email,
            phone=employee_data.phone,
            department_id=employee_data.department_id,
            designation=employee_data.designation,
            joining_date=employee_data.joining_date,
            status=employee_data.status,
            admin_user_id=current_user.id,
        )

        return employee

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.patch(
    "/{employee_id}/deactivate",
    response_model=EmployeeResponse,
)
def deactivate_employee_route(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    employee = get_employee_by_id(
        db=db,
        employee_id=employee_id,
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    if employee.status == "INACTIVE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee is already inactive",
        )

    return deactivate_employee(
        db=db,
        employee=employee,
        admin_user_id=current_user.id,
    )
    
