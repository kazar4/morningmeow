import tkinter
from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('./chromedriver')

root = Tk()

root.geometry("900x600")

global image_num
image_num = 0

global startingPage, cat_page
startingPage = 1
cat_page = "https://pixabay.com/images/search/cat/?pagi={}&"

#req = requests.get(cat_page.format(startingPage))
#page_html = req.content

driver.get(cat_page.format(startingPage))
page_html = driver.page_source

html_dump = BeautifulSoup(page_html, 'html.parser')
#print(html_dump)

global link_list

link_list = []
for t in html_dump.find_all('img'):
    if "cdn.pixabay.com" in t.get("src"):
        link_list.append(t.get("src"))

for t in link_list:
    print(t)

res = requests.get(
  'https://images.pexels.com/photos/437886/pexels-photo-437886.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940')

target_h = 500

# Create a photoimage object of the image in the path
image1 = Image.open(BytesIO(res.content))
w, h = image1.size

if h > 500:
    mul = 500/h

image1 = image1.resize((int(w*mul), int(h*mul)))

test = ImageTk.PhotoImage(image1)

label1 = tkinter.Label(image=test)
label1.image = test

def addImage():
    print("image added")
    next_image()

def skipImage():
    global image_num
    print("image skipped")
    next_image()

def next_image():
    global image_num
    image_num = image_num + 1

    if image_num > len(link_list) - 1:
        image_num = 0
        next_page()

    res = requests.get(link_list[image_num])
    target_h = 500

    # Create a photoimage object of the image in the path
    image1 = Image.open(BytesIO(res.content))
    w, h = image1.size

    mul = 1
    if h > target_h:
        mul = target_h/h

    image1 = image1.resize((int(w*mul), int(h*mul)))
    test = ImageTk.PhotoImage(image1)
    label1.configure(image=test)
    #label1 = tkinter.Label(image=test)
    label1.image = test

def next_page():
    global startingPage, link_list
    startingPage = startingPage + 1

    driver.get(cat_page.format(startingPage))
    page_html = driver.page_source

    html_dump = BeautifulSoup(page_html, 'html.parser')
    #print(html_dump)

    link_list = []
    for t in html_dump.find_all('img'):
        if "cdn.pixabay.com" in t.get("src"):
            link_list.append(t.get("src"))

    for t in link_list:
        print(t)

useButton = tkinter.Button(root, text ="Use", command = addImage, width = 50, height = 5, bg = "green")
useButton.pack(anchor = "s", side = "left")

skipButton = tkinter.Button(root, text ="Skip", command = skipImage, width = 50, height = 5, bg = "red")
skipButton.pack(anchor = "s", side = "right")

# Position image
label1.place(x=0, y=0)
root.mainloop()