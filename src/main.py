#region ------- IMPORTS -------------------------------------------------------------------------------------

from fastapi import FastAPI, HTTPException
import requests

#endregion ---- IMPORTS -------------------------------------------------------------------------------------

#region ------- CONSTANTS -----------------------------------------------------------------------------------

# Declare basic constants for API functioning
BASE_ENDPOINT = 'https://jsonplaceholder.typicode.com'
USERS_ENDPOINT = '/users'
TODOS_ENDPOINT = '/todos'

#endregion ---- CONSTANTS -----------------------------------------------------------------------------------

#region ------- UTILS ---------------------------------------------------------------------------------------

#endregion ---- UTILS --------------------------------------------------------------------------------------

#region ------- INIT ----------------------------------------------------------------------------------------

# Initialize FastAPI
app = FastAPI()

#endregion ---- INIT ----------------------------------------------------------------------------------------

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

#endregion ---- ROUTES -------------------------------------------------------------------------------------