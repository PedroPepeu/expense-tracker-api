from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import auth, database, models, schemas

router = APIRouter(tags=["Expenses"])


@router.post("/expenses/", response_model=schemas.ExpenseOut)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    new_expense = models.Expense(**expense.dict(), user_id=current_user.id)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/expenses/", response_model=List[schemas.ExpenseOut])
def get_expenses(
    filter_date: str = Query("all", enum=["week", "month", "3months", "custom", "all"]),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    query = db.query(models.Expense).filter(models.Expense.user_id == current_user.id)

    now = datetime.now()

    if filter_date == "week":
        query = query.filter(models.Expense.date >= now - timedelta(days=7))
    elif filter_date == "month":
        query = query.filter(models.Expense.date >= now - timedelta(days=30))
    elif filter_date == "3months":
        query = query.filter(models.Expense.date >= now - timedelta(days=90))
    elif filter_date == "custom":
        query = query.filter(
            models.Expense.date >= start_date, models.Expense.date <= end_date
        )

    return query.all()


@router.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    expense = (
        db.query(models.Expense)
        .filter(
            models.Expense.id == expense_id, models.Expense.user_id == current_user.id
        )
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return {"detail": "Expense deleted"}
