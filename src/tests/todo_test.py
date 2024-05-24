#region ------- IMPORTS -------------------------------------------------------------------------------------

from fastapi.testclient import TestClient
from src import main

#endregion ---- IMPORTS -------------------------------------------------------------------------------------

#region ------- INIT ----------------------------------------------------------------------------------------

client = TestClient(main.app)

#endregion ---- INIT ----------------------------------------------------------------------------------------

#region ------- CONSTANTS -----------------------------------------------------------------------------------

FIRST_TODO = {
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "completed": False
}
VALIDATION_ERROR_DESCR = "Validation Error - Query parameters must be positive integers"
MISSING_PARAM_ERROR_DETAIL = [{'type': 'missing', 'loc': ['query', 'userId'], 'msg': 'Field required', 'input': None}]
FLOAT_PARSING_ERROR_DETAIL = [{'type': 'int_parsing', 'loc': ['query', 'userId'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': "25.3"}]

#endregion ---- CONSTANTS -----------------------------------------------------------------------------------

#region ------- TESTS ---------------------------------------------------------------------------------------

# Test GET /todos endpoint with default parameters (and for user 1)
def test_default_request():
    response = client.get("/todos?userId=1")
    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response.json()) == 5, f"Error in query limit parameter - Expected 5 results, got {len(response.json())}"
    assert response.json()[0]['userId'] == FIRST_TODO['userId'], f"Error in query offset - Expected userId {FIRST_TODO['userId']}, got {response.json()[0]['userId']}"
    assert response.json()[0]['id'] == FIRST_TODO['id'], f"Error in query offset - Expected userId {FIRST_TODO['id']}, got {response.json()[0]['id']}"
    assert response.json()[0]['completed'] == FIRST_TODO['completed'], f"Error in query offset - Expected userId {FIRST_TODO['completed']}, got {response.json()[0]['completed']}"

# Test GET /todos endpoint with no user id provided
def test_noUserId_request():
    response = client.get("/todos")
    assert response.status_code == 422, f"Error in fetching data - Expected 422, got {response.status_code}"
    assert response.json()['detail'] == MISSING_PARAM_ERROR_DETAIL, f"Error in setting result description - Expected [{MISSING_PARAM_ERROR_DETAIL}], got [{response.json()['detail']}]"
    # Add other params
    response = client.get("/todos?limit=5&offset=10")
    assert response.status_code == 422, f"Error in fetching data - Expected 422, got {response.status_code}"
    assert response.json()['detail'] == MISSING_PARAM_ERROR_DETAIL, f"Error in setting result description - Expected [{MISSING_PARAM_ERROR_DETAIL}], got [{response.json()['detail']}]"

# Test GET /todos endpoint with a negative userId (this should not fail because there are no defined constraint for userId except for it being an integer)
def test_negativeUserId_request():
    response = client.get("/todos?userId=-53")
    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response.json()) == 0, f"Error in query limit parameter - Expected 0 results, got {len(response.json())}"
    # Set userId to 0 and add other parameters
    response = client.get("/todos?userId=0&limit=10")
    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response.json()) == 0, f"Error in query limit parameter - Expected 0 results, got {len(response.json())}"

# Test GET /todos endpoint with a non-integer userId
def test_nonIntegerUserId_request():
    response = client.get("/todos?userId=25.3")
    assert response.status_code == 422, f"Error in fetching data - Expected 422, got {response.status_code}"
    assert response.json()['detail'] == FLOAT_PARSING_ERROR_DETAIL, f"Error in setting result description - Expected [{FLOAT_PARSING_ERROR_DETAIL}], got [{response.json()['detail']}]"

# Test GET /todos endpoint for a user with no todos
def test_noTodo_request():
    response = client.get("/todos?userId=11")
    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response.json()) == 0, f"Error in query limit parameter - Expected 0 results, got {len(response.json())}"

# Test GET /todos endpoint with personalized query parameters
def test_personalized_request():
    response = client.get("/todos?userId=1&limit=2&offset=6")
    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response.json()) == 2, f"Error in query limit parameter - Expected 2 results, got {len(response.json())}"
    assert response.json()[0]['id'] == 7, f"Error in query offset - Expected id {7}, got {response.json()[0]['id']}"
    # Invert query parameters
    response = client.get("/users?offset=6&limit=2")
    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response.json()) == 2, f"Error in query limit parameter - Expected 2 results, got {len(response.json())}"
    assert response.json()[0]['id'] == 7, f"Error in query offset - Expected id {7}, got {response.json()[0]['id']}"

# Test GET /users endpoint with limit bigger than total elements
def test_biggerLimit_request():
    response = client.get("/todos?userId=5&limit=30")
    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response.json()) == 20, f"Error in query limit parameter - Expected 30 results, got {len(response.json())}"
    assert response.json()[0]['id'] == 81, f"Error in query offset - Expected id {81}, got {response.json()[0]['id']}"
    assert response.json()[9]['userId'] == 5, f"Error in query offset - Expected userId {5}, got {response.json()[0]['userId']}"

# Test GET /users endpoint with offset bigger than total elements
def test_biggerOffset_request():
    response = client.get("/users?offset=100")
    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response.json()) == 0, f"Error in query limit parameter - Expected 0 results, got {len(response.json())}"

# Test GET /users endpoint with invalid query parameters
def test_invalid_request():
    # Negative limit
    response = client.get("/todos?userId=1&limit=-2&offset=6")
    assert response.status_code == 422, f"Error in catching invalid values - Expected 422, got {response.status_code}"
    assert response.json()['detail'] == VALIDATION_ERROR_DESCR, f"Error in setting result description - Expected [{VALIDATION_ERROR_DESCR}], got [{response.json()['detail']}]"
    # Zero limit
    response = client.get("/todos?userId=1&limit=0&offset=6")
    assert response.status_code == 422, f"Error in catching invalid values - Expected 422, got {response.status_code}"
    assert response.json()['detail'] == VALIDATION_ERROR_DESCR, f"Error in setting result description - Expected [{VALIDATION_ERROR_DESCR}], got [{response.json()['detail']}]"
    # Negative offset
    response = client.get("/todos?userId=1&limit=2&offset=-5")
    assert response.status_code == 422, f"Error in catching invalid values - Expected 422, got {response.status_code}"
    assert response.json()['detail'] == VALIDATION_ERROR_DESCR, f"Error in setting result description - Expected [{VALIDATION_ERROR_DESCR}], got [{response.json()['detail']}]"

#endregion ---- TESTS ---------------------------------------------------------------------------------------