#region ------- IMPORTS -------------------------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

#endregion ---- IMPORTS -------------------------------------------------------------------------------------

#region ------- INIT ----------------------------------------------------------------------------------------

# Init base declarative class for SQL table
Base = declarative_base()

#endregion ---- INIT ----------------------------------------------------------------------------------------
#region ------- MODEL ---------------------------------------------------------------------------------------

# Table model for SQL db
class RequestLog(Base):
    __tablename__ = 'request_logs'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    route = Column(String, nullable=False)
    ip_sender = Column(String, nullable=False)
    query = Column(String, nullable=True)
    body = Column(String, nullable=True)
    result_code = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

#endregion ---- MODEL ---------------------------------------------------------------------------------------