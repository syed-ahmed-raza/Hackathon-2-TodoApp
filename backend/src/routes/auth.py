from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
import security, models
from database import get_db

router = APIRouter(tags=["auth"])

@router.post("/signup")
async def signup(request: Request, db: Session = Depends(get_db)):
    # 1. Data Receive Karein (JSON ya Form Data, jo bhi ho)
    try:
        body = await request.json() # Pehle JSON try karein
    except:
        try:
            form = await request.form() # Agar JSON nahi, to Form try karein
            body = dict(form)
        except:
            raise HTTPException(status_code=422, detail="Invalid data format")

    # 2. Email aur Password nikalein (Smart Search)
    # Frontend shayad 'email' bhej raha hai ya 'username', hum dono check karenge
    email = body.get("email") or body.get("username")
    password = body.get("password")

    # 3. Validation
    if not email:
        raise HTTPException(status_code=422, detail="Email field is missing in request body")
    if not password:
        raise HTTPException(status_code=422, detail="Password field is missing in request body")

    # 4. Check existing user
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # 5. Create User
    hashed_password = security.get_password_hash(password)
    new_user = models.User(email=email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

@router.post("/login", response_model=models.Token)
async def login(request: Request, db: Session = Depends(get_db)):
    # Login ke liye bhi same "Smart" tareeqa
    try:
        body = await request.json()
    except:
        form = await request.form()
        body = dict(form)
        
    email = body.get("username") or body.get("email")
    password = body.get("password")

    if not email or not password:
         raise HTTPException(status_code=422, detail="Email/Username or Password missing")

    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user or not security.verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}