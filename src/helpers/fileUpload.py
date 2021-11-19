from flask import request
import os, uuid

def saveImage(fieldName: str, directory: str):
    if fieldName not in request.files:
        raise Exception('Invalid file field name provided')

    # CHECK IF PROFILE IMAGES DIRECTORY EXISTS
    if not os.path.exists("src/" + directory):
        os.makedirs("src/" + directory)

    # OBTAIN IMAGE PROVIDED IN REQUEST AND SAVE IT WITH AN UNIQUE NAME
    image = request.files[fieldName]
    imageName = uuid.uuid4().hex + image.filename
    imageRoute = os.path.join(directory, imageName)
    image.save("src/" + imageRoute)
    
    # CONCATENATE SERVER'S BASE URL WITH THE IMAGE ROUTE FOR STORING IT IN THE DATABASE
    imageRoute = os.getenv('BASE_URL') + imageRoute

    return imageRoute

def deleteImage(imageURL: str):
    # CHECK IF PROFILE IMAGE ROUTE EXISTS
    imageRoute = "src/" + imageURL.split(os.getenv('BASE_URL'))[1]

    if not os.path.exists(imageRoute):
        return
    else:
        os.remove(imageRoute)
        return