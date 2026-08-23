from fastapi import APIRouter, HTTPException, Depends, Response, status, Request
from fastapi.responses import RedirectResponse
from ..oauth import oauth
from authlib.integrations.starlette_client import OAuthError
router = APIRouter(prefix="/api/auth/google", tags=["Authentication"])


@router.get("/login", name="login")
async def user_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri, prompt="select_account")

@router.get("/callback", name="google_callback")
async def google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google authentication failed")

    user = token["userinfo"]
    return {"user_detail":
            {
                "google_id": user["sub"],
                "name": user["name"],
                "email": user["email"],
                "picture": user["picture"]
            } 
    }
