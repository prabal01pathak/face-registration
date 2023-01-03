import base64
from uuid import uuid4
import shutil
from io import BytesIO

from PIL import Image
import numpy as np
import face_recognition

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    BackgroundTasks,
    status,
    WebSocket,
)


from starlette.middleware.cors import CORSMiddleware

from utils import (
    load_encodings,
    get_encodings_and_keys,
    write_encodings,
    save_encodings,
    save_user_data,
    load_user_data
)

from schema import UserData, ImageData

MIN_DISTANCE = 0.4

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
async def recognition(
    data: UserData,
    # image_file: UploadFile = File(...)
) -> dict:
    """register the user"""
    # img = face_recognition.api.load_image_file(image_file.file, mode="RGB")
    image = await process_image_bytes(data.image_text)
    data = data.dict()
    data.pop("image_text")
    print("user data: ", data)
    return await process_image(img=image, user_data=data)


@app.post("/recognize")
async def recognition(
    data: ImageData
):
    """ recognize the face and get the data from json"""
    image = await process_image_bytes(image_text=data.image_text)
    return await get_user_data(img=image)

async def get_user_data(img):
    face_encodings = face_recognition.api.face_encodings(
        img, known_face_locations=None, num_jitters=1, model="cnn"
    )
    total_faces = len(face_encodings)
    if total_faces != 1:
        print(f"{total_faces} faces found")
        return {"found": False, "total_faces": total_faces}
    data = load_encodings()
    known_encodings, keys = get_encodings_and_keys(data=data)
    found_face, is_temp = False, True
    if len(known_encodings) != 0:
        face_distance = face_recognition.api.face_distance(
            known_encodings, face_to_compare=face_encodings[0]
        )
        key = np.argmin(face_distance)
        print("keys: ", key)
        if face_distance[key] <= MIN_DISTANCE:
            print("gettting the user data")
            data = load_user_data()
            return data[keys[key]]
    return {}

async def process_image(img, user_data: dict):
    face_encodings = face_recognition.api.face_encodings(
        img, known_face_locations=None, num_jitters=1, model="cnn"
    )
    total_faces = len(face_encodings)
    if total_faces != 1:
        print(f"{total_faces} faces found")
        return {"found": False, "total_faces": total_faces}
    faceid = uuid4().hex
    data = load_encodings()
    known_encodings, keys = get_encodings_and_keys(data=data)
    found_face, is_temp = False, True
    if len(known_encodings) != 0:
        face_distance = face_recognition.api.face_distance(
            known_encodings, face_to_compare=face_encodings[0]
        )
        key = np.argmin(face_distance)
        if face_distance[key] <= MIN_DISTANCE:
            # if len(data[keys[key]]) < 5:
            #     print("written the image again")
            #     write_encodings(encoding=face_encodings, key=keys[key])
            return {"message": "face id alreaady exists", "status": False}
    write_encodings(encoding=face_encodings[0], key=faceid)
    save_user_data(user_id=faceid, user_data=user_data)
    return {"message": "registerd user successfully", "status": True, "faceid": faceid}

async def process_image_bytes(
    image_text: str
) -> dict:
    """
    The process_image_bytes function takes in a base64 image,
    glass number, and the path to save the image.
    It saves the base64 image as an actual jpg file at that path location.
    It then overlays a transparent
    image of glasses over that saved jpg file and returns it as a b64 encoded string.
    :param **kwargs: Used to Pass a variable number of keyword arguments to the function.
    :return: A dictionary with the key "b64_image" and value of a base64 encoded image.
    :doc-author: Trelent
    """
    _im = Image.open(BytesIO(base64.b64decode(image_text)))
    image = get_np_array_from_tar_object(image_file=_im)
    return image

def get_np_array_from_tar_object(image_file):
    """converts a buffer from a tar file in np.array"""
    return np.array(image_file)