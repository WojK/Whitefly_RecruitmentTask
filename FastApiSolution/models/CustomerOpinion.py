from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base


class CustomerOpinion(Base):
    __tablename__ = "customerOpinion"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True),
                        default=func.now())
    name = Column(String)
    text = Column(String)
