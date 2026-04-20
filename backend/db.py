from  collections.abc import AsyncGenerator
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime


#change it to .env
DATABASE_URL = "postgresql+asyncpg://mikolaj:mikolaj@localhost:5432/dziennik"

class Base(DeclarativeBase):
    pass


class LectureClass(Base):
    __tablename__ = "classes_table1"
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_number = Column(Integer, nullable=False)
    class_desc = Column(Text, nullable=False)
    student_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        

async def get_async_session() -> AsyncGenerator[AsyncSession,None]:
    async with async_session_maker() as session:
        yield session