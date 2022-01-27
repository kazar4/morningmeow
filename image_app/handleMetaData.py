import os
import os.path
from pathlib import Path

# requires exiftool to be on file path
def changeImageComment(image_path, comment):
    return os.system('exiftool.exe -XPComment="{}" {}'.format(comment, image_path))

def addPictureMeta(dir, link, author):
    XPComment = 'Photo by <a href=\'{}\'>{}</a>'.format(link, author)
    changeImageComment(dir, XPComment)