import datetime, uuid
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, default=str(uuid.uuid4()))
    type = Column(String)
    status = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.now)
    input_file = Column(String, nullable=True)
    result_file = Column(String, nullable=True)
    shot = Column(Integer)
