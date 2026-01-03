from fastapi import FastAPI
from sqlalchemy import create_engine, String, Integer,select
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column,load_only
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL","sqlite:///./test.db")
engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
app = FastAPI()


class Test(Base):
    __tablename__ = "test"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


Base.metadata.create_all(bind=engine)


@app.get("/test/{name}")
async def test_save(name: str):
    db = SessionLocal()
    try:
        new_row = Test(name=name)
        db.add(new_row)
        db.commit()
        db.refresh(new_row)
        return {"name": new_row.name}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()



        
