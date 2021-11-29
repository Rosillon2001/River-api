#named this class cloudinaryAPI because 'cloudinary' generates trouble
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import jsonify

def upload(filename:str):
    uploadResult = cloudinary.uploader.upload(filename)
    print(jsonify(uploadResult))
    return jsonify(uploadResult)
