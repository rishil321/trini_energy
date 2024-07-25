import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker


url = URL.create(
    drivername="postgresql",
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_URL"),
    database=os.getenv("DB_NAME"),
    port=5432,
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()
