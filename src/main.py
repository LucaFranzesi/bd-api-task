#region ------- IMPORTS -------------------------------------------------------------------------------------

from fastapi import FastAPI, HTTPException, Request, Depends
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timezone
from src.models import Base, RequestLog

#endregion ---- IMPORTS -------------------------------------------------------------------------------------

#region ------- CONSTANTS -----------------------------------------------------------------------------------

# Default value to use when not running inside Docker
DATABASE_URL = "postgresql://lucaf:1234@localhost:5432/http_db"

# Declare basic constants for API functioning
BASE_ENDPOINT = 'https://jsonplaceholder.typicode.com'
USERS_ENDPOINT = '/users'
TODOS_ENDPOINT = '/todos'

#endregion ---- CONSTANTS -----------------------------------------------------------------------------------


#region ------- UTILS ---------------------------------------------------------------------------------------

def get_session_local():
    yield SessionLocal()

#endregion ---- UTILS ---------------------------------------------------------------------------------------

#region ------- INIT ----------------------------------------------------------------------------------------

# Initialize FastAPI
app = FastAPI()

# Initialize DB and create it if not existing
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

#endregion ---- INIT ----------------------------------------------------------------------------------------

#region ------- MIDDLEWARE ----------------------------------------------------------------------------------

@app.middleware("http")
async def log_request(request: Request, call_next):
    response = await call_next(request)
    session = SessionLocal()

    try:
        log_entry = RequestLog(
            type=request.method,
            route=request.url.path,
            ip_sender=request.client.host,
            query=str(request.query_params),
            body=(await request.body()).decode("utf-8"),
            result_code=(response.status_code),
            timestamp=datetime.now(timezone.utc)
        )
        session.add(log_entry)
        session.commit()
    finally:
        session.close()

    return response

#endregion ---- MIDDLEWARE ----------------------------------------------------------------------------------

#region ------- ROUTES --------------------------------------------------------------------------------------

# GET request for users from a mock service identified by [BASE_ENDPOINT] + [USER_ENDPOINT]
@app.get("/users")
async def get_users(limit: int = 5, offset: int = 0):
    """Gets and returns a list of users

    Parameters
    ----------
    limit : int
        
        Limit to number of results returned from the request (default is 5)
    
    offset : int
        
        Offset to data returned by the query (default is 0)

    Returns
    -------
    data : list
        
        A list of users with their attributes, paginated by limit and offset

    Notes
    -------
    Throws all classic HTTP FastAPI exceptions plus:
        
        - Error code 422 - Validation Error - When limit is 0 or less or offset is less than 0

        - Error code 500 - Internal Server Error - When the API cannot correctly invoke the Mock API
    """

    # Handle bad parameters
    if limit <= 0 or offset < 0:
        raise HTTPException(status_code=422, detail="Validation Error - Query parameters must be positive integers")
    
    # Invoke Mock API
    response = requests.get(BASE_ENDPOINT + USERS_ENDPOINT)

    # Parse values received or raise Exception in case of error
    if(response.status_code == 200):
        data = response.json()
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error - Could not communicate with jsonplaceholder API")
    
    # Return data paginated
    return data[offset : offset + limit]

# GET request for todos endpoint from a mock service identified by [BASE_ENDPOINT] + [TODOS_ENDPOINT]
@app.get("/todos")
async def get_todos(userId: int, limit: int = 5, offset: int = 0):
    """Gets and returns a list of todos for a specific user

    Parameters
    ----------
    userId: int

        Id of the user who created todos we want to get (note: only bound in values it can assume is integer)

    limit : int
        
        Limit to number of results returned from the request (default is 5)
    
    offset : int
        
        Offset to data returned by the query (default is 0)

    Returns
    -------
    data : list
        
        A list of todos for a specific user with their attributes, paginated by limit and offset

    Notes
    -------
    Throws all classic HTTP FastAPI exceptions plus:
        
        - Error code 422 - Validation Error - When limit is 0 or less or offset is less than 0

        - Error code 500 - Internal Server Error - When the API cannot correctly invoke the Mock API
    """

    # Handle bad parameters
    if limit <= 0 or offset < 0:
        raise HTTPException(status_code=422, detail="Validation Error - Query parameters must be positive integers")
    
    # Invoke Mock API
    response = requests.get(BASE_ENDPOINT + TODOS_ENDPOINT, params={'userId' : userId})

    # Parse values received or raise Exception in case of error
    if(response.status_code == 200):
        data = response.json()
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error - Could not communicate with jsonplaceholder API")
    
    return data[offset : offset + limit]

@app.get("/db_logs")
async def get_logs(offset: int = 0, limit: int = 10, db: Session = Depends(get_session_local)):
    logs = db.query(RequestLog).offset(offset).limit(limit).all()
    return logs

#endregion ---- ROUTES -------------------------------------------------------------------------------------