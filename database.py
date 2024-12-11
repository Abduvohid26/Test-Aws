from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, BigInteger

DATABASE_URL = "postgresql+asyncpg://bot_user:2629@localhost:5432/bot_db"

# Asosiy baza konfiguratsiyasi
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# User modeli
class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    chat_id = Column(BigInteger, unique=True, nullable=False)

# Baza yaratish
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



