from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
import security, models
from database import get_db

router = APIRouter(tags=["auth"])

@router.post("/signup")
def signup(user_data: models.UserCreate, db: Session = Depends(get_db)):
    # ✅ FIX: Check karein ke email hai ya username
    user_email = user_data.email or user_data.username
    
    if not user_email:
        raise HTTPException(status_code=422, detail="Email is required")

    # 1. Check existing user
    user = db.query(models.User).filter(models.User.email == user_email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # 2. Hash Password
    hashed_password = security.get_password_hash(user_data.password)
    
    # 3. Save User
    new_user = models.User(email=user_email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

@router.post("/login", response_model=models.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}