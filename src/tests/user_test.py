#region ------- IMPORTS -------------------------------------------------------------------------------------

from fastapi.testclient import TestClient
from src import main

#endregion ---- IMPORTS -------------------------------------------------------------------------------------

#region ------- INIT ----------------------------------------------------------------------------------------

client = TestClient(main.app)

#endregion ---- INIT ----------------------------------------------------------------------------------------

#region ------- CONSTANTS -----------------------------------------------------------------------------------

FIRST_USER = {
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
      "street": "Kulas Light",
      "suite": "Apt. 556",
      "city": "Gwenborough",
      "zipcode": "92998-3874",
      "geo": {
        "lat": "-37.3159",
        "lng": "81.1496"
      }
    },
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "company": {
      "name": "Romaguera-Crona",
      "catchPhrase": "Multi-layered client-server neural-net",
      "bs": "harness real-time e-markets"
    }
}
VALIDATION_ERROR_DESCR = "Validation Error - Query parameters must be positive integers"
NOTFOUND_ERROR_DESCR = "Not Found"
INTEGER_PARSING_ERROR_DETAIL = [{'type': 'int_parsing', 'loc': ['query', 'limit'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': "'test'"}]
FLOAT_PARSING_ERROR_DETAIL = [{'type': 'int_parsing', 'loc': ['query', 'offset'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': "2.4"}]

#endregion ---- CONSTANTS -----------------------------------------------------------------------------------

#region ------- TESTS ---------------------------------------------------------------------------------------

# Test GET /users endpoint with default parameters
def test_default_request():
    response = client.get("/users")
    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response.json()) == 5, f"Error in query limit parameter - Expected 5 results, got {len(response.json())}"
    assert response.json()[0]['id'] == FIRST_USER['id'], f"Error in query offset - Expected userId {FIRST_USER['id']}, got {response.json()[0]['id']}"
    assert response.json()[0]['name'] == FIRST_USER['name'], f"Error in query offset - Expected userName {FIRST_USER['name']}, got {response.json()[0]['name']}"
    assert response.json()[0]['phone'] == FIRST_USER['phone'], f"Error in query offset - Expected userPhone {FIRST_USER['phone']}, got {response.json()[0]['phone']}"
    assert response.json()[0]['address']['street'] == FIRST_USER['address']['street'], f"Error in query offset - Expected userId {FIRST_USER['address']['street']}, got {response.json()[0]['address']['street']}"

# Test GET /users endpoint with wrong route
def test_wrongRoute_request():
    response = client.get("/user")
    assert response.status_code == 404, f"Error in fetching data - Expected 404, got {response.status_code}"
    assert response.json()['detail'] == NOTFOUND_ERROR_DESCR, f"Error in setting result description - Expected [{NOTFOUND_ERROR_DESCR}], got [{response.json()['detail']}]"

# Test GET /users endpoint with personalized query parameters
def test_personalized_request():
    response = client.get("/users?limit=2&offset=6")
    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response.json()) == 2, f"Error in query limit parameter - Expected 2 results, got {len(response.json())}"
    assert response.json()[0]['id'] == 7, f"Error in query offset - Expected userId {7}, got {response.json()[0]['id']}"
    # Invert query parameters
    response = client.get("/users?offset=6&limit=2")
    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response.json()) == 2, f"Error in query limit parameter - Expected 2 results, got {len(response.json())}"
    assert response.json()[0]['id'] == 7, f"Error in query offset - Expected userId {7}, got {response.json()[0]['id']}"

# Test GET /users endpoint with invalid query parameters
def test_invalid_request():
    # Negative limit
    response = client.get("/users?limit=-2&offset=6")
    assert response.status_code == 422, f"Error in catching invalid values - Expected 422, got {response.status_code}"
    assert response.json()['detail'] == VALIDATION_ERROR_DESCR, f"Error in setting result description - Expected [{VALIDATION_ERROR_DESCR}], got [{response.json()['detail']}]"
    # Zero limit
    response = client.get("/users?limit=0&offset=6")
    assert response.status_code == 422, f"Error in catching invalid values - Expected 422, got {response.status_code}"
    assert response.json()['detail'] == VALIDATION_ERROR_DESCR, f"Error in setting result description - Expected [{VALIDATION_ERROR_DESCR}], got [{response.json()['detail']}]"
    # Negative offset
    response = client.get("/users?limit=2&offset=-5")
    assert response.status_code == 422, f"Error in catching invalid values - Expected 422, got {response.status_code}"
    assert response.json()['detail'] == VALIDATION_ERROR_DESCR, f"Error in setting result description - Expected [{VALIDATION_ERROR_DESCR}], got [{response.json()['detail']}]"

# Test GET /users endpoint with limit bigger than total elements
def test_biggerLimit_request():
    response = client.get("/users?limit=25")
    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response.json()) == 10, f"Error in query limit parameter - Expected 25 results, got {len(response.json())}"
    assert response.json()[0]['id'] == 1, f"Error in query offset - Expected userId {1}, got {response.json()[0]['id']}"
    assert response.json()[9]['id'] == 10, f"Error in query offset - Expected userId {10}, got {response.json()[0]['id']}"

# Test GET /users endpoint with offset bigger than total elements
def test_biggerOffset_request():
    response = client.get("/users?offset=100")
    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response.json()) == 0, f"Error in query limit parameter - Expected 0 results, got {len(response.json())}"

# Test GET /users endpoint with wrong parameters type
def test_wrongTypes_request():
    #Limit string type
    response = client.get("/users?limit='test'")
    assert response.status_code == 422, f"Error in fetching data - Expected 422, got {response.status_code}"
    assert response.json()['detail'] == INTEGER_PARSING_ERROR_DETAIL, f"Error in setting result description - Expected [{INTEGER_PARSING_ERROR_DETAIL}], got [{response.json()['detail']}]"
    #Offset float type
    response = client.get("/users?offset=2.4")
    assert response.status_code == 422, f"Error in fetching data - Expected 422, got {response.status_code}"
    assert response.json()['detail'] == FLOAT_PARSING_ERROR_DETAIL, f"Error in setting result description - Expected [{FLOAT_PARSING_ERROR_DETAIL}], got [{response.json()['detail']}]"

#endregion ---- TESTS ---------------------------------------------------------------------------------------