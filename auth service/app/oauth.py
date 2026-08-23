from fastapi import Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from .config import settings

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)
