from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
import security, models  
from database import get_db

router = APIRouter(
    tags=["auth"],
)

# 👇 FIX: Wapas OAuth2PasswordRequestForm laga diya (Frontend Form Data bhej raha hai)
@router.post("/signup")
def signup(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Note: Frontend 'email' bhej raha hai, lekin Form Data mein wo 'username' field mein aata hai
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Password Hash karein
    hashed_password = security.get_password_hash(form_data.password)
    
    # User Save karein (email = form_data.username)
    new_user = models.User(email=form_data.username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

@router.post("/login")
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