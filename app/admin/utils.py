import os
from flask import current_app
import secrets


#Define a function to save student images
def save_student_image(picture):
    #randomize the name of image(making each image unique)
    random_hex = secrets.token_hex(10)
    
    #Grab the file extension of the uploaded image
    _, file_ext = os.path.splitext(picture.filename)
    
    #Combine the random hex with the file extension to get a new file name
    picture_name = random_hex + file_ext
    
    #Define a picture path 
    picture_path = os.path.join(current_app.root_path, 'static/assets/images/users_profile', picture_name)
    
    #Save the image in a specified folder
    picture.save(picture_path)
    
    return picture_name
    
#Define a function to save teacher images
def save_teacher_image(picture):
    #randomize the name of image(making each image unique)
    random_hex = secrets.token_hex(10)
    
    #Grab the file extension of the uploaded image
    _, file_ext = os.path.splitext(picture.filename)
    
    #Combine the random hex with the file extension to get a new file name
    picture_name = random_hex + file_ext
    
    #Define a picture path 
    picture_path = os.path.join(current_app.root_path, 'static/assets/images/users_profile', picture_name)
    
    #Save the image in a specified folder
    picture.save(picture_path)
    
    return picture_name

#Define a function to save user images
def save_user_image(picture):
    #randomize the name of image(making each image unique)
    random_hex = secrets.token_hex(10)
    
    #Grab the file extension of the uploaded image
    _, file_ext = os.path.splitext(picture.filename)
    
    #Combine the random hex with the file extension to get a new file name
    picture_name = random_hex + file_ext
    
    #Define a picture path 
    picture_path = os.path.join(current_app.root_path, 'static/assets/images/users_profile', picture_name)
    
    #Save the image in a specified folder
    picture.save(picture_path)
    
    return picture_name
    