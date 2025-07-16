# --------Imports--------
from json import load, dump
from re import sub, compile, findall, search, IGNORECASE
from pprint import pprint
from ollama import chat
from rapidfuzz import process
from pydantic import BaseModel, RootModel, field_validator
from typing import List, Dict, Tuple
from deep_translator import GoogleTranslator

from sys import stdout
stdout.reconfigure(encoding='utf-8')


# --------Classes--------


class BoxFeeling(BaseModel):
    up_down: List[str] = []
    left_right: List[str] = []
    front_back: List[str] = []
    overall: List[str] = []

    def __add__(self, other):
        if isinstance(other, BoxFeeling):
            return BoxFeeling(
                up_down=self.up_down + other.up_down,
                left_right=self.left_right + other.left_right,
                front_back=self.front_back + other.front_back,
                overall=self.overall + other.overall,
            )
        else:
            raise TypeError(
                f"Unsupported operand type(s) for +: 'BoxFeeling' and '{type(other).__name__}'")


class BoxDescription(BaseModel):
    weight: List[float] = []
    feeling: BoxFeeling = BoxFeeling()

    def __add__(self, other):
        if isinstance(other, BoxDescription):
            return BoxDescription(
                weight=self.weight + other.weight,
                feeling=self.feeling + other.feeling
            )
        else:
            raise TypeError(
                f"Unsupported operand type(s) for +: 'BoxDescription' and '{type(other).__name__}'")

    def to_json(self):
        return """{
            "weight": %s,
            "feeling": {
                "up-down": %s,
                "left-right": %s,
                "front-back": %s,
                "overall": %s,
            }
        }""" % (self.weight, self.feeling.up_down, self.feeling.left_right, self.feeling.front_back, self.feeling.overall)


class BlindBox(RootModel[Dict[str, BoxDescription]]):
    name: str
    description: BoxDescription = BoxDescription()

    def __add__(self, other):
        if isinstance(other, BlindBox):
            if self.name != other.name:
                raise ValueError("BlindBoxes must have the same name")
            return BlindBox(
                name=self.name,
                description=self.description + other.description
            )
        else:
            raise TypeError(
                f"Unsupported operand type(s) for +: 'BlindBox' and '{type(other).__name__}'")

    def to_json(self):
        return """{
            '%s': {
                "description": {
                    "weight": %s,
                    "feeling": {
                        "up-down": %s,
                        "left-right": %s,
                        "front-back": %s,
                        "overall": %s,
                    }
                }
            }
        }""" % (
            self.name,
            self.description.weight,
            self.description.feeling.up_down,
            self.description.feeling.left_right,
            self.description.feeling.front_back,
            self.description.feeling.overall
        )


class ResponseObject(RootModel[List[BlindBox]]):
    pass

# --------Functions--------


def filter_description(description: str) -> str:
    """
    This function takes a string description and removes any unneeded characters
    and symbols from it, returning a cleaner string.

    :param description: The string description to be cleaned
    :return: A cleaner string description
    """
    # Remove Hashtags
    description = sub(r"#([^\n\t.!]+)", "", description)
    # Remove @mentions
    description = sub(r"@([^\n\t.!]+)", "", description)

    return description


def gather_data(desc: str):
    prompt = """
    You are an expert in analyzing the description of blind boxes.
    Your task is to analyze a post description of blind boxs and extract the following information for each box as a JSON object:
    [
        "blind box character": {
            "description": {
                "weight": [],
                "feeling": {
                    "up-down": [],
                    "left-right": [],
                    "front-back": [],
                    "overall": [],
                }
            }
        },
    ]
       
    
    if no information or characters are found, return an empty list -> [].
       
    """
    schema = ResponseObject.model_json_schema()
    # pprint(schema)
    response = chat(
        model="llama3.2",
        # model="deepseek-r1",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": desc}
        ],
        format=schema
    )
    try:
        return ResponseObject.model_validate(eval(response.message.content))
    except Exception as e:
        print(e)
        print(response.message.content)
        return ResponseObject([])


# --------Main--------
luffy_pattern = compile(r'(luffy|路飞)', IGNORECASE)
translator = GoogleTranslator(source='zh-CN', target='en')

# --------Get Data--------
# Gathering Descriptions (en/zh)
if False:
    # Loading data
    posts: dict = load(open('./res/output.json', 'r', encoding='utf-8'))
    en_description = open('./res/txts/description.txt', 'w+', encoding='utf-8')
    zh_description = open('./res/txts/description_zh.txt',
                          'w+', encoding='utf-8')
    # Writing data
    for post in posts.values():
        # Filtering
        en = filter_description(post['description']['en'])
        zh = filter_description(post['description']['zh'])
        # Checks for trades
        if match := search(r"change", en, flags=IGNORECASE):
            continue
        # Checks for luffy
        if luffy_pattern.search(en) or luffy_pattern.search(zh):
            en_description.write(en + '\n')
            zh_description.write(zh + '\n')
    # Closing
    en_description.close()
    zh_description.close()

# --------Process Data--------
"""_summary_
This is where we take the post description data and process it
by cleaning the data and either sending it to the AI 
or spliting the data by one piece characters before sending it to the AI
"""


# --------Artifical Intelligence--------

if True:
    descriptions = open('./res/txts/description.txt',
                        'r', encoding='utf-8').readlines()
    character_json = {}

    for i, description in enumerate(descriptions):
        if not luffy_pattern.search(description):
            # print("Skipping...")
            continue

        print(f"Processing {i}/{len(descriptions)}")
        data = gather_data(description)

        for box in data.root:
            print(box)
            if box.name not in character_json:
                character_json[box.name] = box.description
            else:
                character_json[box.name] += box.description

    # --------Save Data--------
    for name, description in character_json.items():
        character_json[name] = description.model_dump()
    dump(character_json, open('./res/jsons/character.json', 'w+', encoding='utf-8'))

# --------Translate--------
if False:
    keys = list(character_json.keys())
    for name in keys:
        new_name = translator.translate(name)
        character_json[new_name] = character_json.pop(name)
    dump(character_json, open('./res/jsons/character.json', 'w+', encoding='utf-8'))
