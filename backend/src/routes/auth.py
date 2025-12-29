from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
import security, models  # ✅ Import sahi hai
from database import get_db

router = APIRouter(
    tags=["auth"],
)

# 👇 SIGNUP FIX: JSON data accept karne ke liye UserCreate model use karein
@router.post("/signup")
def signup(user_data: models.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # ✅ FIX: 'auth' ki jagah 'security' use kiya
    hashed_password = security.get_password_hash(user_data.password)
    
    new_user = models.User(email=user_data.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # ✅ FIX: 'auth' ki jagah 'security' use kiya
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # ✅ FIX: 'auth' ki jagah 'security' use kiya
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}