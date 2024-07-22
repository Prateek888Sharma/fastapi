from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app import schemas, database, models
from .config import settings
from fastapi import Depends, status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

 #secret key
 #algorithm
 #expiration time of token

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')  #tokenurl specifies from which endpoint JWT token can be obtained for authentication

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    token = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM )
    
    return token

def verify_token(token:str, credentials_exception) -> schemas.TokenData:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id :str = payload.get("user_id")

        if not id:

            raise credentials_exception
        
        token_data = schemas.TokenData(id=str(id))
        return token_data

    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")

    except JWTError:
        raise credentials_exception
    
def get_current_user(token:str=Depends(oauth_scheme), db:Session=Depends(database.get_db)) -> models.User:
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = f"Could not validate Credentials",
                                        headers={"WWW-Authenticate":"Bearer"})
    
   
    token = verify_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user