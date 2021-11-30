#named this class cloudinaryAPI because 'cloudinary' generates trouble
from cloudinary import uploader

def upload(file, folder, imageName):
    uploadResult = uploader.upload(file, folder = f'river/'+folder, public_id = imageName)
    
    return uploadResult

def delete(file):
    noURI = file.split('/river/')[1]
    fileName = 'river/'+noURI.split('.')[0]+'.'+noURI.split('.')[1]
    deletionResult = uploader.destroy(fileName)

    return deletionResult