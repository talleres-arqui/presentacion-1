from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Datos de conexión a tu MySQL (ajusta según docker-compose)
DATABASE_URL = "mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
