from pydantic import BaseModel


class UserData(BaseModel):
    """ user data schema"""
    name: str
    email: str
    phone_number: str
    govt_id_number: str
    image_text: str


class ImageData(BaseModel):
    """ image data"""
    image_text: str