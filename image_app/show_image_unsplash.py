import tkinter
from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO
from handleMetaData import *
from unidecode import unidecode

import sys
sys.path.insert(1, '../morningmeow')
from util import readAuthFiles

root = Tk()
root.geometry("900x600")

global image_num, startingPage, link_list, unsplash_access_key, unsplash_secret_key

currentImage = ""

unsplash_access_key = readAuthFiles("../morningmeow/authFiles.txt")["unsplash_access_key"]
unsplash_secret_key = readAuthFiles("../morningmeow/authFiles.txt")["unsplash_secret_key"]

image_num = 95
startingPage = 70
label1 = tkinter.Label()
link_list = []

def addImage():
    global image_num, link_list, currentImage
    #print("image added")
    print(link_list[image_num])

    save_image(currentImage, link_list[image_num][1], unidecode(link_list[image_num][2]))
    next_image()

def skipImage():
    #print("image skipped")
    next_image()

def next_image():
    global image_num, link_list, currentImage
    image_num = image_num + 1

    if image_num > len(link_list) - 1:
        image_num = 0
        next_page()

    res = requests.get(link_list[image_num][0])
    target_h = 500

    # Create a photoimage object of the image in the path
    image1 = Image.open(BytesIO(res.content))
    w, h = image1.size

    mul = 1
    if h > target_h:
        mul = target_h/h

    image1 = image1.resize((int(w*mul), int(h*mul)))

    currentImage = image1

    test = ImageTk.PhotoImage(image1)
    label1.configure(image=test)
    #label1 = tkinter.Label(image=test)
    label1.image = test

def next_page():
    global startingPage, link_list, unsplash_access_key, unsplash_secret_key
    startingPage = startingPage + 5

    print("next page")

    link = "https://api.unsplash.com/search/photos?page={}&query=cat&per_page=300&client_id={}"
    res = requests.get(link.format(startingPage, unsplash_access_key))
    json_data = res.json()["results"]

    for val in json_data:
        image_link = val["urls"]["regular"]
        image_website = val["links"]["html"].strip()
        image_author = val["user"]["name"].strip()

        tup = (image_link, image_website, image_author)
        #print(tup)

        link_list.append(tup)

def save_image(img, link, author):
    global image_num, startingPage
    save_location = f"../images/{image_num}-{startingPage}.jpg"

    img.save(f"../images/{image_num}-{startingPage}.jpg")
    addPictureMeta(save_location, link, author)

next_page()
next_image()

useButton = tkinter.Button(root, text ="Use", command = addImage, width = 50, height = 5, bg = "green")
useButton.pack(anchor = "s", side = "left")

skipButton = tkinter.Button(root, text ="Skip", command = skipImage, width = 50, height = 5, bg = "red")
skipButton.pack(anchor = "s", side = "right")

# Position image
label1.place(x=0, y=0)
root.mainloop()