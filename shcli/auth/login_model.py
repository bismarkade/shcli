from pydantic import BaseModel

class LoginModel(BaseModel):
    """ A model to validate the login details"""
    client_id: str 
    client_secret: str
