from pydantic import BaseModel, HttpUrl

class RequestURL(BaseModel):
    long_url : HttpUrl
    