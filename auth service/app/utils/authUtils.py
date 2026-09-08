from fastapi import Depends, HTTPException, status, Request, Response
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import usersModel, authModel
from ..schemas import userSchemas, authSchemas
from ..config import settings
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
import uuid

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/google/login')

def create_access_token(data: authSchemas.AccessToken) -> str:
    to_encode = data.model_dump()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode, algorithm=settings.algorithm, key=settings.secret_key)
    return encoded_jwt


def get_create_user(token_data: userSchemas.UserData, db: Session):
    user = db.query(usersModel.User).filter(usersModel.User.google_sub == token_data.sub).first()
    if user is None:
        user = usersModel.User(
            google_sub=token_data.sub,
            email=token_data.email
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    login_id = str(uuid.uuid4())
    user_id = user.user_id
    refresh_token_data = authSchemas.RefreshToken(
        user_id=user_id,
        login_id=login_id
    )
    access_token_data = authSchemas.AccessToken(
        user_id=user.user_id,
        login_id=login_id
    )
    access_token = create_access_token(access_token_data)
    refresh_token = create_refresh_token(refresh_token_data)

    new_token_entry = authModel.Token(
    token_hash = password_hash.hash(refresh_token),
    login_id = login_id
    )
    try:
        db.add(new_token_entry)    
        db.commit()
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Could not create login session')

    return {'access_token':access_token, 'refresh_token':refresh_token}


def verify_access_token(jwt_token: str, credentials_exception, db:Session):
    try:
        token_payload = jwt.decode(token=jwt_token, algorithms=settings.algorithm, key=settings.secret_key)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired",
                            headers={"WWW-Authenticate" : "Bearer"})
    except JWTError as e:
        raise credentials_exception
    
    if token_payload.get('token_type') != "access_token":
        raise credentials_exception

    user_id = token_payload['user_id']
    if not user_id:
        raise credentials_exception

    session_entry = db.query(authModel.Token).filter(authModel.Token.login_id==token_payload['login_id']).first()
    if not session_entry:
        raise credentials_exception
    
    token_data = authSchemas.AccessToken(**token_payload)
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token",
                                            headers={"WWW-Authenticate" : "Bearer"})
    token_data = verify_access_token(token, credentials_exception=credentials_exception, db=db)
    user = db.query(usersModel.User).filter(usersModel.User.user_id == token_data.user_id).first()
    if not user:
        raise credentials_exception
    user_data_out = userSchemas.UserDataOut.model_validate(user)
    return user_data_out


def create_refresh_token(token_data: authSchemas.RefreshToken, expire:datetime | None = None) -> str:
    to_encode = token_data.model_dump()
    if expire is None:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({'exp': expire, 'jti':str(uuid.uuid4())})
    refresh_token = jwt.encode(to_encode, key=settings.secret_key, algorithm=settings.algorithm)
    return refresh_token


def verify_refresh_token(request: Request, db:Session=Depends(get_db)):
    request_refresh_token = request.cookies.get('refresh_token')
    print('refresh_token: ', request_refresh_token)
    if request_refresh_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
    try:
        token_payload = jwt.decode(request_refresh_token, key=settings.secret_key, algorithms=settings.algorithm, options={'verify_exp':False})
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')

    if token_payload.get('token_type') != "refresh_token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')

    token_login_id = token_payload.get('login_id')    
    query = db.query(authModel.Token).filter(authModel.Token.login_id == token_login_id)
    token_entry = query.first()

    if datetime.now(timezone.utc).timestamp() > token_payload.get('exp'):
        if token_entry is not None:
            query.delete(synchronize_session=False)
            db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token has expired')

    if token_entry is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
    
    if not password_hash.verify(request_refresh_token, token_entry.token_hash):
        query.delete(synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')

    query.delete(synchronize_session='auto')
    refresh_token_data = authSchemas.RefreshToken(**token_payload)
    expiry = token_payload.get('exp')
    new_refresh_token = create_refresh_token(refresh_token_data, expire=expiry)
    new_token_entry = authModel.Token(
        token_hash = password_hash.hash(new_refresh_token),
        login_id = token_login_id
    )
    db.add(new_token_entry)
    db.commit()

    access_token_data = authSchemas.AccessToken(user_id=refresh_token_data.user_id, 
                                                login_id=refresh_token_data.login_id)    
    new_access_token = create_access_token(access_token_data)
    return {'access_token':new_access_token, 'refresh_token':new_refresh_token}


def get_login_id(token:str=Depends(oauth2_scheme)):
    try:
        token_payload = jwt.decode(token=token, algorithms=settings.algorithm, key=settings.secret_key, options={'verify_exp':False})
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')
    
    if token_payload.get('token_type') != "access_token" or not token_payload.get('login_id'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')

    return token_payload.get('login_id')