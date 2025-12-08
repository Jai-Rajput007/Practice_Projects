# app/routers/files.py
from fastapi import APIRouter, Depends, Header, HTTPException, status, Cookie
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import datetime, timezone  # Import timezone for robust datetime comparisons
from .. import database, models, security

router = APIRouter(prefix="/api/files", tags=["Files"])


async def get_valid_session_and_verify_proof(
    session_id: Annotated[str, Cookie()] = None,
    x_session_proof: Annotated[str, Header()] = "",
    db: Session = Depends(database.get_db)
):
    """
    This is the core security dependency. It performs several checks:
    1. Ensures a session cookie exists.
    2. Validates the session against the database (exists and not expired).
    3. Fetches user and session details for the proof calculation.
    4. Calculates the server-side proof hash and compares it to the client's.
    5. If all checks pass, it increments the round number for the next request.
    """
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # 1. Look up the session in the database
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    
    # 2. Validate the session's existence and expiry (using timezone-aware comparison)
    if not session or session.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session invalid or expired")

    # 3. Get the associated user to fetch their secret key
    user = db.query(models.User).filter(models.User.id == session.user_id).first()
    # Added robustness: check if user was deleted but session somehow remained
    if not user:
        raise HTTPException(status_code=401, detail="User for session not found")

    user_secret = user.user_secret_key
    round_number = session.current_round_number

    # 4. --- CORE CYCLIC PROOF VERIFICATION ---
    server_proof = security.create_cyclic_proof_hash(round_number, user_secret)
    if server_proof != x_session_proof:
        # LOG THIS FAILED ATTEMPT IN A REAL APPLICATION!
        raise HTTPException(status_code=401, detail="Invalid Session Proof. Request blocked.")

    # 5. Success! Update the round number for the next request.
    session.current_round_number += 1
    db.commit()

    # Return the necessary data for the main endpoint to use
    return {
        "user_id": session.user_id,
        "next_round_number_for_client": session.current_round_number
    }


@router.get("/my-files")
def list_my_files(session_data: dict = Depends(get_valid_session_and_verify_proof)):
    """
    An example protected endpoint that lists dummy files for the authenticated user.
    This function only runs if the 'get_valid_session_and_verify_proof' dependency succeeds.
    """
    # The session_data from the dependency contains the next round number.
    # We must construct and return a JSON response for the client.
    return {
        "message": f"Successfully accessed files for user {session_data['user_id']}",
        "files": ["file1.txt", "document.pdf", "image.jpg"],
        "next_round_number": session_data['next_round_number_for_client']
    }