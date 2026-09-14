from pydantic import BaseModel

class inputs(BaseModel):
    name: str
    email: str
    password: str