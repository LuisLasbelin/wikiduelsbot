#!/usr/bin/python3
from datetime import date
from flask import Flask, render_template
import requests

APP = Flask(__name__)

SESSION = requests.Session()
ENDPOINT = "https://en.wikipedia.org/w/api.php"

@APP.route("/")
def index():
    # get today date
    todays_date = date.today().isoformat()

    data = fetch_potd(todays_date)

    return render_template("index.html", data=data)

def fetch_potd(cur_date):
    date_iso = cur_date
    title = "Template:POTD_protected/" + date_iso

    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "images",
        "titles": title
    }

    response = SESSION.get(url = ENDPOINT, params = params)
    data = response.json()
    filename = data["query"]["pages"][0]["images"][0]["title"]
    image_page_url = "https://en.wikipedia.org/wiki/" + title

    image_data = {
    "filename": filename,
    "image_page_url": image_page_url,
    "image_src": fetch_image_src(filename),
    "date": date_iso
    }

    return image_data

def fetch_image_src(filename):
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "titles": filename
    }

    response = SESSION.get(url = ENDPOINT, params = params)
    data = response.json()
    page = next(iter(data["query"]["pages"].values()))
    image_info = page["imageinfo"][0]
    image_url = image_info["url"]

    return image_url

if __name__ == "__main__":
  APP.run()