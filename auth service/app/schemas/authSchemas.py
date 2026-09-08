from pydantic import BaseModel

class RefreshToken(BaseModel):
    token_type: str = "refresh_token"
    login_id: str
    user_id: int


class AccessToken(BaseModel):
    token_type: str = "access_token"
    user_id: int
    login_id: str
    model_config = {'from_attributes': True}