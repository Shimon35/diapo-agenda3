import xml.etree.ElementTree as ET
import json
import html
import re
from datetime import datetime


RSS_FILE = "agenda.rss"
JSON_FILE = "agenda.json"


# Namespace utilisé par OpenAgenda
NS = {
    "ev": "http://purl.org/rss/1.0/modules/event/"
}


def clean_html(text):
    if not text:
        return ""

    text = html.unescape(text)

    # Suppression des balises HTML
    text = re.sub(r"<[^>]+>", " ", text)

    # Nettoyage des espaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_text(element, tag, namespace=None):

    if namespace:
        child = element.find(
            f"{{{namespace}}}{tag}"
        )
    else:
        child = element.find(tag)

    if child is None:
        return ""

    return child.text or ""


# ---------------------------------------------------------
# Lecture RSS
# ---------------------------------------------------------

tree = ET.parse(RSS_FILE)
root = tree.getroot()

channel = root.find("channel")

events = []


for item in channel.findall("item"):

    title = get_text(item, "title")

    description = get_text(item, "description")

    link = get_text(item, "link")

    guid = get_text(item, "guid")

    start = get_text(
        item,
        "startdate",
        NS["ev"]
    )

    end = get_text(
        item,
        "enddate",
        NS["ev"]
    )

    location = get_text(
        item,
        "location",
        NS["ev"]
    )


    # -----------------------------------------------------
    # IMAGE
    # -----------------------------------------------------

    image = None

    enclosure = item.find("enclosure")

    if enclosure is not None:

        image = enclosure.get("url")


    # -----------------------------------------------------
    # Création événement
    # -----------------------------------------------------

    event = {

        "uid": guid,

        "title": {
            "fr": title
        },

        "description": {
            "fr": clean_html(description)
        },

        "start": start,

        "end": end,

        "location": {
            "name": location
        },

        "image": image,

        "link": link

    }


    events.append(event)


# ---------------------------------------------------------
# Création JSON
# ---------------------------------------------------------

data = {

    "total": len(events),

    "events": events

}


with open(
    JSON_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        data,
        f,
        ensure_ascii=False,
        indent=2
    )


print(
    f"{len(events)} événements enregistrés dans {JSON_FILE}"
)
