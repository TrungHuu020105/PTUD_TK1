"""
Test script for To-Do List API (Cấp 4)
Can be run with: python test_api.py
"""
import requests
import json
from typing import Any

BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}


def print_response(title: str, response: requests.Response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"TEST: {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2, default=str)}")
    except:
        print(f"Response: {response.text}")


def main():
    print("\n" + "="*60)
    print("TO-DO LIST API - CẤAP 4 TEST")
    print("="*60)

    # 1. Create todos
    print("\n1. CREATE TODOS")
    todo1_data = {
        "title": "Learn FastAPI",
        "description": "Study FastAPI with SQLAlchemy",
        "is_done": False
    }
    r1 = requests.post(f"{BASE_URL}/todos", json=todo1_data, headers=HEADERS)
    print_response("Create Todo 1", r1)
    todo1_id = r1.json()["id"]

    todo2_data = {
        "title": "Setup Database",
        "description": "Configure SQLite and migrations",
        "is_done": False
    }
    r2 = requests.post(f"{BASE_URL}/todos", json=todo2_data, headers=HEADERS)
    print_response("Create Todo 2", r2)
    todo2_id = r2.json()["id"]

    # 2. List todos
    r_list = requests.get(f"{BASE_URL}/todos", headers=HEADERS)
    print_response("List All Todos", r_list)

    # 3. Get single todo
    r_get = requests.get(f"{BASE_URL}/todos/{todo1_id}", headers=HEADERS)
    print_response(f"Get Todo {todo1_id}", r_get)

    # 4. PATCH todo (partial update) - NEW
    patch_data = {"is_done": True}
    r_patch = requests.patch(f"{BASE_URL}/todos/{todo1_id}", json=patch_data, headers=HEADERS)
    print_response("PATCH Todo (update is_done)", r_patch)

    # 5. PATCH with description update
    patch_data = {"description": "Updated via PATCH"}
    r_patch2 = requests.patch(f"{BASE_URL}/todos/{todo2_id}", json=patch_data, headers=HEADERS)
    print_response("PATCH Todo (update description)", r_patch2)

    # 6. Complete todo - NEW
    r_complete = requests.post(f"{BASE_URL}/todos/{todo2_id}/complete", headers=HEADERS)
    print_response("POST /todos/{id}/complete", r_complete)

    # 7. Full update (PUT)
    put_data = {
        "title": "Learn FastAPI - Advanced",
        "description": "Deep dive with ORM and migrations",
        "is_done": False
    }
    r_put = requests.put(f"{BASE_URL}/todos/{todo1_id}", json=put_data, headers=HEADERS)
    print_response("PUT Todo (full update)", r_put)

    # 8. Search/filter todos
    r_search = requests.get(f"{BASE_URL}/todos?q=FastAPI", headers=HEADERS)
    print_response("GET Todos with search (q=FastAPI)", r_search)

    # 9. Filter by is_done
    r_filter = requests.get(f"{BASE_URL}/todos?is_done=true", headers=HEADERS)
    print_response("GET Todos filtered by is_done=true", r_filter)

    # 10. Sort and pagination
    r_sorted = requests.get(f"{BASE_URL}/todos?sort=-created_at&limit=10&offset=0", headers=HEADERS)
    print_response("GET Todos sorted by -created_at with pagination", r_sorted)

    # 11. Delete todo
    r_delete = requests.delete(f"{BASE_URL}/todos/{todo1_id}", headers=HEADERS)
    print_response(f"DELETE Todo {todo1_id}", r_delete)

    # 12. Final list
    r_final = requests.get(f"{BASE_URL}/todos", headers=HEADERS)
    print_response("GET Todos (final list)", r_final)

    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the API is running on http://localhost:8000")
