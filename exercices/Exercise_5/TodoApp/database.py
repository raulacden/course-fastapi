import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Postgres123!@localhost/TodoApplicationDatabase'
SQLALCHEMY_DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    'postgresql://deploy_database_0uyw_user:gEYIyEulspra3BacZTCqRiHbmAfJTTFt@dpg-d8ntfob7uimc738a54v0-a.frankfurt-postgres.render.com/deploy_database_0uyw',
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
