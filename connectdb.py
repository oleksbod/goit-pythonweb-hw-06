from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

# Встановлюємо параметри підключення до PostgreSQL
DB_URL = "postgresql://postgres:05071984@localhost:5432/hw06"

# Створюємо об'єкт engine для підключення до бази даних
engine = create_engine(DB_URL)
# Створюємо сесію
session = Session(engine)


Base = declarative_base()