# imports
from ollama import chat
from pydantic import BaseModel, RootModel, field_validator
from typing import List, Dict, Tuple
from deep_translator import GoogleTranslator
import json
import numpy as np
from pprint import pprint
import urllib
import os

from sys import stdout
stdout.reconfigure(encoding='utf-8')


# Use images to gather blind box information

data: dict = json.loads(
    open('./res/output.json', 'r', encoding='utf-8').read())

images = np.array([img for post in data.values() for img in post['images']])
media_path = './res/media/'

# download images
# for image in images:
#     if not os.path.exists(media_path + image):
#         urllib.request.urlretrieve(image, media_path + image)

for url in data.keys():
    print(url)
