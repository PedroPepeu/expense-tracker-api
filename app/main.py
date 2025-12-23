from fastapi import FastAPI

from . import database, models
from .routers import auth, expenses

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Expense Tracker API")

app.include_router(auth.router)
app.include_router(expenses.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Expense Tracker API"}
