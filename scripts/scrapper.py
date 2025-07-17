# --------Imports--------
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import time
import re
import os
import requests
import json
from pprint import pprint

import sys
sys.stdout.reconfigure(encoding='utf-8')

# --------Functions--------


def get_driver(headless=False):
    """
    Creates a new instance of the Chrome driver.

    Args:
        headless (bool): Whether to run the driver in headless mode.

    Returns:
        undetected_chromedriver.Chrome: The Chrome driver.
    """
    # Create a new instance of ChromeOptions
    options = uc.ChromeOptions()

    if headless:
        options.add_argument('--headless=new')

    options.add_argument('--disable-blink-features=AutomationControlled')

    return uc.Chrome(
        # Pass the options to the Chrome driver
        options=options,
        browser_executable_path=r'.\res\chrome\chrome-win64\chrome.exe',

        # Specify the path to the chromedriver
        driver_executable_path=r'.\res\chrome\chromedriver.exe',
        version_main=138,
        # Specify the user data directory
        user_data_dir=r'.\res\chrome\User Data',

    )


def scrape_posts(query: str):
    driver.get(f"https://www.xiaohongshu.com/search_result?keyword={query}")
    url = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",  # You can replace this with your browser's
    }

    cookies = {cookie['name']: cookie['value']
               for cookie in driver.get_cookies()}
    data_json = {}

    i = 1
    while True:
        payload = {
            "keyword": query,
            "page": i,
            "search_id": "2f0xhxrpf1op8z97mez8o3i8",
            "page_size": 20,
            "sort": "general",
        }
        try:
            response = requests.post(
                url, json=payload, headers=headers, cookies=cookies)
            data = response.json()
            if data['data']['has_more']:
                for post in data['data']['items']:
                    if post['model_type'] != 'note':
                        continue

                    data_json[post['id']] = post

                print(f'page {i}')
            else:
                print('Done')
                break
        except Exception as e:
            print(e)

        i += 1

    return data_json


def scrape_post(url: str, id: str):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Get description
    description = soup.find('meta', {'name': 'description'})['content']

    # Get Image if available
    images = [s['content']
              for s in soup.find_all('meta', {'name': 'og:image'})]

    # Get Videos if available
    videos = [s['content']
              for s in soup.find_all('meta', {'name': 'og:video'})]

    return description, images, videos


def extract_useful_sentences(raw_text):
    KEYWORDS = ['weight', 'shake', 'box', 'feel',
                'obstruction', 'desiccant', 'sway', 'sound']
    sentences = re.split(r'[.!?]\s*', raw_text)
    return [s.strip() for s in sentences if any(k in s.lower() for k in KEYWORDS)]


# --------Data--------
global driver
driver = get_driver(headless=False)
translator = GoogleTranslator(source='auto', target='en')


if __name__ == "__main__":
    query = 'Labubu One Piece Weights'
    data: dict = json.load(open('./res/data.json', 'r', encoding='utf-8'))

    # Obtain posts
    if False:
        for post in scrape_posts(query).values():
            data[post['id']] = {
                "xsec_token": post['xsec_token'],
                "description": '',
                "images": [],
                "videos": [],
                "likes": post['note_card']['interact_info']['liked_count'],
            }
        json.dump(data, open('./res/data.json',
                  'w', encoding='utf-8'), indent=4)

    # Scrape posts
    if True:
        for id, post in data.items():
            d, i, v = scrape_post(
                f'https://www.xiaohongshu.com/explore/{id}?xsec_token={post["xsec_token"]}',
                id
            )
            post['description'] = d
            post['images'] = i
            post['videos'] = v

        json.dump(data, open('./res/data.json',
                  'w', encoding='utf-8'), indent=4)
if False:
    from datetime import datetime
    import pytz

    # Define the China Standard Time (CST) timezone
    china_timezone = pytz.timezone('Asia/Shanghai')

    # Get the current time in the specified timezone
    china_time = datetime.now(china_timezone)
