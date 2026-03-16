"""
Test script for To-Do List API - Cấp 5 (Authentication)
Tests: Register → Login → Get Me → Create Todo → List Todos
Run with: python test_cap5.py
"""
import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}


def print_response(title: str, response: requests.Response, show_body: bool = True):
    """Pretty print API response"""
    print(f"\n{'='*70}")
    print(f"TEST: {title}")
    print(f"{'='*70}")
    print(f"Status: {response.status_code}")
    if show_body:
        try:
            data = response.json()
            print(f"Response:\n{json.dumps(data, indent=2, default=str)}")
        except:
            print(f"Response: {response.text}")


def main():
    print("\n" + "="*70)
    print("TO-DO LIST API - CẤAP 5 TEST (Authentication + User Separation)")
    print("="*70)

    # 1. Register User 1
    print("\n[STEP 1] Register User 1")
    user1_data = {
        "email": "alice@example.com",
        "password": "alice123456"
    }
    r_register1 = requests.post(f"{BASE_URL}/auth/register", json=user1_data, headers=HEADERS)
    print_response("Register User 1", r_register1)
    user1_id = r_register1.json()["id"]

    # 2. Register User 2
    print("\n[STEP 2] Register User 2")
    user2_data = {
        "email": "bob@example.com",
        "password": "bob123456"
    }
    r_register2 = requests.post(f"{BASE_URL}/auth/register", json=user2_data, headers=HEADERS)
    print_response("Register User 2", r_register2)
    user2_id = r_register2.json()["id"]

    # 3. Login User 1
    print("\n[STEP 3] Login User 1")
    r_login1 = requests.post(f"{BASE_URL}/auth/login", json=user1_data, headers=HEADERS)
    print_response("Login User 1", r_login1)
    token1 = r_login1.json()["access_token"]

    # 4. Login User 2
    print("\n[STEP 4] Login User 2")
    r_login2 = requests.post(f"{BASE_URL}/auth/login", json=user2_data, headers=HEADERS)
    print_response("Login User 2", r_login2)
    token2 = r_login2.json()["access_token"]

    # 5. Get Me (User 1)
    print("\n[STEP 5] Get Current User (User 1)")
    headers_user1 = {"Authorization": f"Bearer {token1}"}
    r_me1 = requests.get(f"{BASE_URL}/auth/me", headers={**HEADERS, **headers_user1})
    print_response("Get Me (User 1)", r_me1)

    # 6. Create Todo for User 1
    print("\n[STEP 6] Create Todo (User 1)")
    todo1_data = {
        "title": "Learn Authentication",
        "description": "Understand JWT and user isolation",
        "is_done": False
    }
    r_create1 = requests.post(
        f"{BASE_URL}/todos",
        json=todo1_data,
        headers={**HEADERS, **headers_user1}
    )
    print_response("Create Todo (User 1)", r_create1)
    todo1_id = r_create1.json()["id"]

    # 7. Create Todo for User 2
    print("\n[STEP 7] Create Todo (User 2)")
    headers_user2 = {"Authorization": f"Bearer {token2}"}
    todo2_data = {
        "title": "Read Documentation",
        "description": "Study API design patterns",
        "is_done": False
    }
    r_create2 = requests.post(
        f"{BASE_URL}/todos",
        json=todo2_data,
        headers={**HEADERS, **headers_user2}
    )
    print_response("Create Todo (User 2)", r_create2)
    todo2_id = r_create2.json()["id"]

    # 8. List Todos (User 1 - should only see their own)
    print("\n[STEP 8] List Todos (User 1 - should see only their todo)")
    r_list1 = requests.get(
        f"{BASE_URL}/todos",
        headers={**HEADERS, **headers_user1}
    )
    print_response("List Todos (User 1)", r_list1)
    items1 = r_list1.json()["items"]
    print(f"✓ User 1 sees {len(items1)} todo(s)")

    # 9. List Todos (User 2 - should only see their own)
    print("\n[STEP 9] List Todos (User 2 - should see only their todo)")
    r_list2 = requests.get(
        f"{BASE_URL}/todos",
        headers={**HEADERS, **headers_user2}
    )
    print_response("List Todos (User 2)", r_list2)
    items2 = r_list2.json()["items"]
    print(f"✓ User 2 sees {len(items2)} todo(s)")

    # 10. User 1 tries to access User 2's todo (should fail)
    print("\n[STEP 10] Security Test: User 1 tries to access User 2's todo")
    r_access_fail = requests.get(
        f"{BASE_URL}/todos/{todo2_id}",
        headers={**HEADERS, **headers_user1}
    )
    print_response("User 1 GET /todos/{todo2_id} (should be 404)", r_access_fail)
    if r_access_fail.status_code == 404:
        print("✓ SECURITY OK: User cannot access other user's todo")
    else:
        print("✗ SECURITY FAIL: User should not see other user's todo!")

    # 11. User 2 accesses their own todo (should work)
    print("\n[STEP 11] User 2 accesses their own todo")
    r_access_ok = requests.get(
        f"{BASE_URL}/todos/{todo2_id}",
        headers={**HEADERS, **headers_user2}
    )
    print_response("User 2 GET /todos/{todo2_id} (should work)", r_access_ok)

    # 12. PATCH todo (User 2 marks their todo as done)
    print("\n[STEP 12] PATCH Todo (User 2 marks done)")
    patch_data = {"is_done": True}
    r_patch = requests.patch(
        f"{BASE_URL}/todos/{todo2_id}",
        json=patch_data,
        headers={**HEADERS, **headers_user2}
    )
    print_response("PATCH /todos/{todo2_id} (set is_done=true)", r_patch)

    # 13. Complete Todo (User 1 marks their todo as complete)
    print("\n[STEP 13] POST /todos/{todo1_id}/complete")
    r_complete = requests.post(
        f"{BASE_URL}/todos/{todo1_id}/complete",
        headers={**HEADERS, **headers_user1}
    )
    print_response("Complete Todo (User 1)", r_complete)

    # 14. Try creating todo without auth (should fail)
    print("\n[STEP 14] Security Test: Create todo without token")
    r_no_auth = requests.post(
        f"{BASE_URL}/todos",
        json=todo1_data,
        headers=HEADERS
    )
    print_response("POST /todos without Authorization (should be 401)", r_no_auth)
    if r_no_auth.status_code == 401:
        print("✓ SECURITY OK: Cannot create todo without auth")
    else:
        print("✗ SECURITY FAIL: Auth should be required!")

    # 15. Try login with wrong password (should fail)
    print("\n[STEP 15] Security Test: Login with wrong password")
    r_wrong_pass = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "alice@example.com", "password": "wrongpassword"},
        headers=HEADERS
    )
    print_response("Login with wrong password (should be 401)", r_wrong_pass)

    # 16. Final check: Both users' todos are separate
    print("\n[STEP 16] Final check: Each user only sees their todos")
    r_final1 = requests.get(f"{BASE_URL}/todos", headers={**HEADERS, **headers_user1})
    r_final2 = requests.get(f"{BASE_URL}/todos", headers={**HEADERS, **headers_user2})
    
    final_count1 = len(r_final1.json()["items"])
    final_count2 = len(r_final2.json()["items"])
    
    print(f"User 1 final todos: {final_count1}")
    print(f"User 2 final todos: {final_count2}")
    
    if final_count1 == 1 and final_count2 == 1:
        print("✓ PASS: User isolation working correctly!")
    else:
        print(f"✗ FAIL: Expected each user to have 1 todo, got {final_count1} and {final_count2}")

    print("\n" + "="*70)
    print("ALL TESTS COMPLETED")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure the API is running on http://localhost:8000")
