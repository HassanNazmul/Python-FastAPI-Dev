from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Format for Connecting String
# "postgresql://<username>:<password>@<ip-address/hostname>/<database-name>"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
