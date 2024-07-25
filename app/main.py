from fastapi import FastAPI
from .routers import users, groups, expenses
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(groups.router)
app.include_router(expenses.router)
