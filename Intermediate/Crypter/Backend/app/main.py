# app/main.py
from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, files
from fastapi.middleware.cors import CORSMiddleware

# This line creates the database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure Cloud Access Backend")

# --- CORS Middleware ---
# This is crucial for allowing your Next.js frontend to communicate with the backend
origins = [
    "http://localhost:3000",  # Your Next.js frontend
    # Add your production frontend URL here later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routers
app.include_router(auth.router)
app.include_router(files.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Secure Cloud Access API"}