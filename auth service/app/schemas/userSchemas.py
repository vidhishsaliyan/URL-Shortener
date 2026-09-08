from pydantic import BaseModel, EmailStr

class UserData(BaseModel):
    sub: str
    email: EmailStr
    name: str
    model_config = {'from_attributes': True}


class UserDataOut(BaseModel):
    user_id: int
    model_config = {'from_attributes': True}
