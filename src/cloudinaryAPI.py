#named this class cloudinaryAPI because 'cloudinary' generates trouble
from cloudinary import uploader
from flask import jsonify

def upload(file, folder, imageName):
    uploadResult = uploader.upload(file, folder = f'river/'+folder, public_id = imageName)
    
    return uploadResult
