from fastapi import APIRouter, HTTPException, Depends, status, Request, Response
from fastapi.responses import RedirectResponse
from ..oauth2 import oauth
from authlib.integrations.starlette_client import OAuthError
from ..schemas import userSchemas
from ..utils import authUtils
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import usersModel, authModel
from ..utils import authUtils
from jose import jwt, JWTError

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.get("/google/login", name="login")
async def user_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri, prompt="select_account")

@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google authentication failed")

    token_data = userSchemas.UserData.model_validate(token['userinfo'])
    bearer_tokens = authUtils.get_create_user(token_data, db)
    response.set_cookie(
        key="refresh_token",
        value=bearer_tokens.get('refresh_token'),
        httponly=True,
        secure=False,
        samesite='lax'
    )
    return bearer_tokens


@router.post('/refresh', name="refresh_token")
def get_access_refresh_tokens(response: Response, bearer_tokens:dict=Depends(authUtils.verify_refresh_token)):
    response.set_cookie(
    key="refresh_token",
    value=bearer_tokens.get('refresh_token'),
    httponly=True,
    secure=False,
    samesite='lax'
    )
    return bearer_tokens


@router.post('/logout', name="logout")
def delete_user_login(response:Response, db:Session=Depends(get_db), login_id:str=Depends(authUtils.get_login_id)):
    query = db.query(authModel.Token).filter(authModel.Token.login_id == login_id)
    query.delete(synchronize_session=False)
    db.commit()
    response.delete_cookie('refresh_token', path='/api/auth')
    return {"message": "Logged out successfully"}


@router.get('/auth_check')
def test_route(response:  Response, user: userSchemas.UserDataOut = Depends(authUtils.get_current_user)):
    response.headers['X-User-ID'] = str(user.user_id)
    return {'message' : 'Authentication valid'}