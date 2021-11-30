from flask import request
import os, uuid
import cloudinaryAPI

def saveImage(fieldName: str, directory: str):
    if fieldName not in request.files:
        raise Exception('Invalid file field name provided')

    # CHECK IF PROFILE IMAGES DIRECTORY EXISTS
    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    # OBTAIN IMAGE PROVIDED IN REQUEST AND SAVE IT WITH AN UNIQUE NAME
    image = request.files[fieldName]
    imageName = uuid.uuid4().hex + image.filename
    imageRoute = os.path.join(directory, imageName)
    # image.save(imageRoute)
    cloudinaryURI = cloudinaryAPI.upload(image, directory, imageName)
    
    
    # CONCATENATE SERVER'S BASE URL WITH THE IMAGE ROUTE FOR STORING IT IN THE DATABASE
    imageRoute = cloudinaryURI['secure_url']

    return imageRoute

def saveImages(fieldName: str, directory: str):
    print()
    if fieldName not in request.files:
        raise Exception('Invalid file field name provided')

    # CHECK IF PROFILE IMAGES DIRECTORY EXISTS
    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    filesURL = []
    files = request.files.getlist(fieldName)
    for file in files:
        if file.filename != '':
            imageName = uuid.uuid4().hex + file.filename
            imageRoute = os.path.join(directory, imageName)
            # file.save(imageRoute)
            cloudinaryURI = cloudinaryAPI.upload(file, directory, imageName)

            imageRoute = cloudinaryURI['secure_url']
            filesURL.append(imageRoute)
            
    return filesURL



def deleteImage(imageURL: str):
    # CHECK IF PROFILE IMAGE ROUTE EXISTS
    imageRoute = imageURL.split(os.getenv('BASE_URL'))[1]

    if not os.path.exists(imageRoute):
        return
    else:
        os.remove(imageRoute)
        return

