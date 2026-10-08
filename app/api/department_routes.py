# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session

# from app.core.dependencies import require_admin
# from app.database.connection import get_db
# from app.database.models import User

# from app.schemas.department import (
#     DepartmentCreate,
#     DepartmentResponse
# )

# from app.services.department_service import (
#     create_department,
#     get_departments,
#     get_department_by_id
# )


# router = APIRouter(
#     prefix="/api/departments",
#     tags=["Departments"]
# )


# @router.post(
#     "",
#     response_model=DepartmentResponse,
#     status_code=status.HTTP_201_CREATED
# )
# def create_department_endpoint(
#     department_data: DepartmentCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin)
# ):

#     try:
#         department = create_department(
#             db=db,
#             name=department_data.name.strip()
#         )

#         return department

#     except ValueError as error:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail=str(error)
#         )


# @router.get(
#     "",
#     response_model=list[DepartmentResponse]
# )
# def list_departments(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin)
# ):

#     return get_departments(db)


# @router.get(
#     "/{department_id}",
#     response_model=DepartmentResponse
# )
# def get_department(
#     department_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(require_admin)
# ):

#     department = get_department_by_id(
#         db=db,
#         department_id=department_id
#     )

#     if department is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Department not found"
#         )

#     return department





from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.database.connection import get_db
from app.database.models import User
from app.schemas.department import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
)
from app.services.department_service import (
    create_department,
    delete_department,
    get_all_departments,
    get_department_by_id,
    update_department,
)



router = APIRouter(
    prefix="/api/departments",
    tags=["Department Management"],
)


@router.post(
    "",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_department_route(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        department = create_department(
            db=db,
            name=department_data.name,
            admin_user_id=current_user.id,
        )

        return department

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.get(
    "",
    response_model=list[DepartmentResponse],
)
def list_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_all_departments(db=db)


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    department = get_department_by_id(
        db=db,
        department_id=department_id,
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    return department


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse,
)
def update_department_route(
    department_id: int,
    department_data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    department = get_department_by_id(
        db=db,
        department_id=department_id,
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    try:
        department = update_department(
            db=db,
            department=department,
            name=department_data.name,
            admin_user_id=current_user.id,
        )

        return department

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.delete(
    "/{department_id}",
)
def delete_department_route(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    department = get_department_by_id(
        db=db,
        department_id=department_id,
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    try:
        delete_department(
            db=db,
            department=department,
            admin_user_id=current_user.id,
        )

        return {
            "message": "Department deleted successfully",
            "department_id": department_id,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )