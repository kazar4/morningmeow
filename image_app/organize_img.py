

# Go through entire images folder
# get jpegs
# Make a new folder called images_order
# move images into folder in random order but renamed n to n+X
# where n is a number that can be chosen as the starting number and X is the number of jpegs in the folder   

import random
import shutil
import os

dir = "../images"
new_dir = "../images_ordered"

# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f)) and f.endswith(".jpg")]

print(len(onlyfiles))
for i in onlyfiles:
    print(i)

random.shuffle(onlyfiles)

counter = 1
for f in onlyfiles:
    new_f = str(counter) + ".jpg" 
    os.system(f"cp {join(dir,f)} {join(new_dir,new_f)}")
    counter = counter + 1




