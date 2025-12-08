# test_client.py
import requests
import hashlib
import psycopg2
import uuid
import time
from dotenv import load_dotenv
import os

# --- Configuration ---
load_dotenv()
BASE_URL = "http://127.0.0.1:8000"
DATABASE_URL = os.getenv("DATABASE_URL")
SERVER_SECRET_KEY = os.getenv("SERVER_SECRET_KEY")
PUBLIC_INTERMEDIATE_KEY = int(os.getenv("PUBLIC_INTERMEDIATE_KEY"))

# --- Test User Details ---
unique_id = str(uuid.uuid4())[:8]
test_user = {
    "username": f"testuser_{unique_id}",
    "email": f"test_{unique_id}@example.com",
    "password": "strong-password-123"
}

# Use a session object to automatically handle cookies
client = requests.Session()

# --- Helper Functions ---
def print_status(message, is_success):
    """Prints a formatted status message."""
    if is_success:
        print(f"✅ SUCCESS: {message}")
    else:
        print(f"❌ FAILED: {message}")
        # Remove exit() to continue seeing error details

def create_cyclic_proof_hash(round_number: int, user_secret_key: str) -> str:
    """This function must be an exact mirror of the one on the server."""
    value1 = round_number % (PUBLIC_INTERMEDIATE_KEY - 3)
    value2 = round_number % (PUBLIC_INTERMEDIATE_KEY - 2)
    value3 = round_number % (PUBLIC_INTERMEDIATE_KEY - 1)
    combined_string = f"{user_secret_key}-{value1}-{value2}-{value3}-{SERVER_SECRET_KEY}"
    hasher = hashlib.sha256()
    hasher.update(combined_string.encode('utf-8'))
    return hasher.hexdigest()

def get_user_and_session_data_from_db(username):
    """Connects to the DB to fetch secrets needed for the test."""
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Get user secret key
        cur.execute("SELECT id, user_secret_key FROM users WHERE username = %s", (username,))
        user_result = cur.fetchone()
        if not user_result:
            return None, None
        user_id, user_secret = user_result

        # Get session round number
        cur.execute("SELECT current_round_number FROM sessions WHERE user_id = %s ORDER BY created_at DESC LIMIT 1", (user_id,))
        session_result = cur.fetchone()
        if not session_result:
            return user_secret, None
            
        round_number = session_result[0]
        return user_secret, round_number
        
    except Exception as e:
        print(f"Database error: {e}")
        return None, None
    finally:
        if conn:
            conn.close()

# --- Main Test Execution ---
def run_test():
    print("--- STARTING BACKEND INTEGRATION TEST ---")
    
    # 1. Register a new user
    print("\n[1] Attempting to register a new user...")
    print(f"    Sending payload: {test_user}")
    reg_response = client.post(f"{BASE_URL}/api/auth/register", json=test_user)
    print(f"    Status Code: {reg_response.status_code}")
    print(f"    Response Text: {reg_response.text}")
    try:
        print(f"    Response JSON: {reg_response.json()}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"    Failed to parse JSON: {e}")
    print_status("User registration successful.", reg_response.status_code == 201)

    if reg_response.status_code == 201:
        # 2. Login with the new user
        print("\n[2] Attempting to log in...")
        login_payload = {"username": test_user["username"], "password": test_user["password"]}
        print(f"    Sending login payload: {login_payload}")
        login_response = client.post(f"{BASE_URL}/api/auth/login", data=login_payload)
        print(f"    Status Code: {login_response.status_code}")
        print(f"    Response Text: {login_response.text}")
        try:
            print(f"    Response JSON: {login_response.json()}")
        except requests.exceptions.JSONDecodeError as e:
            print(f"    Failed to parse JSON: {e}")
        print_status("Login successful, session cookie should be set.", login_response.status_code == 200)
        # Add a small delay to ensure DB transaction is complete
        time.sleep(1)

        # 3. Fetch secrets from DB to prepare for protected request
        print("\n[3] Fetching secrets from DB for test preparation...")
        user_secret_key, round_number = get_user_and_session_data_from_db(test_user["username"])
        print_status("Successfully fetched user secret and initial round number.", user_secret_key and round_number)
        print(f"    - User Secret (S1) starts with: {user_secret_key[:10]}...")
        print(f"    - Initial Round Number: {round_number}")

        # 4. Make the first protected request
        print("\n[4] Attempting first protected API call...")
        proof = create_cyclic_proof_hash(round_number, user_secret_key)
        headers = {"X-Session-Proof": proof}
        protected_res_1 = client.get(f"{BASE_URL}/api/files/my-files", headers=headers)
        print(f"    Response: {protected_res_1.status_code}, {protected_res_1.json()}")
        print_status("First protected request successful.", protected_res_1.status_code == 200)

        # 5. Make the second protected request
        print("\n[5] Attempting second protected API call with updated round number...")
        if protected_res_1.status_code == 200:
            next_round = protected_res_1.json()["next_round_number"]
            print(f"    - Server provided next round number: {next_round}")
            next_proof = create_cyclic_proof_hash(next_round, user_secret_key)
            headers = {"X-Session-Proof": next_proof}
            protected_res_2 = client.get(f"{BASE_URL}/api/files/my-files", headers=headers)
            print(f"    Response: {protected_res_2.status_code}, {protected_res_2.json()}")
            print_status("Second protected request successful.", protected_res_2.status_code == 200)

        # 6. Logout to destroy the session
        print("\n[6] Attempting to log out...")
        logout_response = client.post(f"{BASE_URL}/api/auth/logout")
        print(f"    Response: {logout_response.status_code}, {logout_response.json()}")
        print_status("Logout successful.", logout_response.status_code == 200)

        # 7. Verify session is destroyed by attempting another protected call
        print("\n[7] Verifying session is destroyed...")
        final_check = client.get(f"{BASE_URL}/api/files/my-files", headers=headers)
        print(f"    Response: {final_check.status_code}")
        print_status("Access denied after logout, as expected.", final_check.status_code == 401)
    
    print("\n--- TEST COMPLETED ---")

if __name__ == "__main__":
    run_test()