import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from typing import Optional
from uuid import uuid4
from database import user_collection
from pydantic import BaseModel
from utils.load_helper import SECRET_KEY

# FastAPI application instance
router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key and algorithm for JWT encoding/decoding
SECRET_KEY = SECRET_KEY  # Use a more secure key in production
ALGORITHM = "HS256"

# JWT expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expires after 30 minutes


# Pydantic models
class SignUpRequest(BaseModel):
    username: str
    kid_name: str
    email: EmailStr
    password: str 
    confirm_password: str
    gender: Optional[str] = None  # Could be 'boy' or 'girl'

    class Config:
        orm_mode = True


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    email: EmailStr
    username: str
    password: str


# Helper function for password hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Helper function for verifying password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Helper function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(signup_data: SignUpRequest):
    # Check if the email is already taken
    existing_user = await user_collection.find_one({"email": signup_data.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered")

    # Check if password and confirm password match
    if signup_data.password != signup_data.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    # Hash the password before saving it
    hashed_password = hash_password(signup_data.password)

    # Create user object and save it to the "user_collection"
    user = {
        "id": str(uuid4()),  # Unique user ID
        "email": signup_data.email,
        "username": signup_data.username,
        "kid_name": signup_data.kid_name,
        "gender": signup_data.gender,
        "password": hashed_password
    }

    # Add user to the collection (in-memory storage)
    user_collection.append(user)

    # Create access token
    access_token = create_access_token(data={"sub": user["email"]})

    return {"message": "User created successfully", "user": {"email": user["email"], "username": user["username"], "kid_name": user["kid_name"]}, "access_token": access_token}


@router.post("/login")
async def login_user(signin_data: SignInRequest):
    # Find user by email
    user = await user_collection.find_one({"email": signin_data.email})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Verify password
    if not verify_password(signin_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    # Create access token
    access_token = create_access_token(data={"sub": user["email"]})

    return {"message": "Login successful", "user": {"email": user["email"], "username": user["username"]}, "access_token": access_token}
