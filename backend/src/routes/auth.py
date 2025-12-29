from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
import security, models
from database import get_db

router = APIRouter(tags=["auth"])

@router.post("/signup")
async def signup(request: Request, db: Session = Depends(get_db)):
    # 1. Data Receive (Magic Way: JSON or Form)
    try:
        body = await request.json()
    except:
        try:
            form = await request.form()
            body = dict(form)
        except:
            raise HTTPException(status_code=422, detail="Invalid data format")

    # 2. Email/Username Extraction
    # Frontend 'email' bhej raha hai, hum wo utha lenge
    email = body.get("email") or body.get("username")
    password = body.get("password")

    if not email or not password:
        raise HTTPException(status_code=422, detail="Email or Password missing")

    # 3. Check Existing User
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 4. Create User
    hashed_password = security.get_password_hash(password)
    new_user = models.User(email=email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

@router.post("/login", response_model=models.Token)
async def login(request: Request, db: Session = Depends(get_db)):
    # Login ke liye bhi same Magic Logic
    try:
        body = await request.json()
    except:
        form = await request.form()
        body = dict(form)
        
    email = body.get("username") or body.get("email")
    password = body.get("password")

    if not email or not password:
         raise HTTPException(status_code=422, detail="Missing credentials")

    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user or not security.verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}