from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
import security, models  # ✅ Humne security.py use kiya hai
from database import get_db

router = APIRouter(
    tags=["auth"],
)

# 👇 SIGNUP: Ab yeh JSON accept karega (Fixed 422 Error)
@router.post("/signup")
def signup(user_data: models.UserCreate, db: Session = Depends(get_db)):
    # 1. Check karein user pehle se to nahi hai
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # 2. Password Hash karein (security file se)
    hashed_password = security.get_password_hash(user_data.password)
    
    # 3. User save karein
    new_user = models.User(email=user_data.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

# 👇 LOGIN: Yeh Form Data hi lega (Standard OAuth2)
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