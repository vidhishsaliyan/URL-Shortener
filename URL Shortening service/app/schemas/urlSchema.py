from pydantic import BaseModel

class RequestURL(BaseModel):
    long_url : str
    