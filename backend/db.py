from  collections.abc import AsyncGenerator
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import os
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from datetime import datetime
from dotenv import load_dotenv
 

# engine = create_async_engine(DATABASE_URL)
# async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
	raise RuntimeError("DATABASE_URL is not set. Add it to backend/.env")


engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
        
# async def get_async_session() -> AsyncGenerator[AsyncSession,None]:
#     async with async_session_maker() as session:
#         yield session