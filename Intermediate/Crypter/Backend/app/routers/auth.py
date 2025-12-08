# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone  # <--- CRITICAL: Import 'timezone'
from .. import database, models, schemas, security
from fastapi.security import OAuth2PasswordRequestForm
import logging

# Basic logging configuration
logging.basicConfig(level=logging.DEBUG)
router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def get_session_id_from_cookie(session_id: Annotated[str, Cookie()] = None):
    """Dependency to get the session_id from the request's cookie."""
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return session_id


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Handles new user registration."""
    # Check if user with that email or username already exists
    if db.query(models.User).filter((models.User.email == user.email) | (models.User.username == user.username)).first():
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    hashed_password = security.get_password_hash(user.password)
    user_secret = security.generate_user_secret()

    new_user = models.User(
        email=user.email,
        username=user.username,
        password_hash=hashed_password,
        user_secret_key=user_secret
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Return a dictionary that matches the UserOut schema explicitly
    return {
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username
    }


@router.post("/login")
def login(response: Response, request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """Handles user login, creates a session, and sets a secure cookie."""
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    # --- THIS IS THE TIMEZONE FIX ---
    session_duration_days = 7
    # Create a timezone-aware "now" timestamp using timezone.utc
    now_utc = datetime.now(timezone.utc)
    # Add the duration to the timezone-aware timestamp
    expires = now_utc + timedelta(days=session_duration_days)
    # ---------------------------------
    
    new_session = models.Session(
        user_id=user.id,
        expires_at=expires,  # Now we are passing a timezone-aware object
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent")
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    # Set the session ID in a secure, HttpOnly cookie
    response.set_cookie(
        key="session_id",
        value=str(new_session.id),
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        expires=expires
    )
    
    # Return a JSON response on success
    return {"status": "success", "message": "Login successful"}


@router.post("/logout")
def logout(response: Response, session_id: str = Depends(get_session_id_from_cookie), db: Session = Depends(database.get_db)):
    """Handles user logout by deleting the session and expiring the cookie."""
    # Delete the session from the database
    db.query(models.Session).filter(models.Session.id == session_id).delete()
    db.commit()
    
    # Instruct the browser to delete the cookie
    response.delete_cookie("session_id")
    return {"status": "success", "message": "Logout successful"}