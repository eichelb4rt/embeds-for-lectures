from __future__ import annotations

import json
from time import sleep
import requests

CONFIG_PATH = "config.json"
LECTURERS_PATH = "lecturers.json"
MODULES_PATH = "modules.json"


def json_get(json_obj, attr):
    return json_obj[attr] if attr in json_obj else None


class Lecturer:
    def __init__(self, name, id, url=None, icon_url=None) -> None:
        self.name = name
        self.id = id
        self.url = url
        self.icon_url = icon_url

    def json(self):
        obj = {
            "name": self.name
        }
        if self.url is not None:
            obj["url"] = self.url
        if self.icon_url is not None:
            obj["icon_url"] = self.icon_url
        return obj

    @staticmethod
    def from_json(json_obj) -> Lecturer:
        return Lecturer(name=json_get(json_obj, "name"),
                        url=json_get(json_obj, "url"),
                        icon_url=json_get(json_obj, "icon_url"),
                        id=json_get(json_obj, "id"))

    @staticmethod
    def from_json_arr(json_arr) -> dict[Lecturer]:
        return {json_obj["id"]: Lecturer.from_json(json_obj) for json_obj in json_arr}


class Module:
    standard_color = 0x000000

    def __init__(self, title, lecturer: Lecturer, color, id=None, url=None, properties: list[str] = None, contents=None, aims=None):
        self.title = title
        self.lecturer = lecturer
        self.color = color
        self.id = id
        self.url = url
        self.properties = properties
        self.contents = contents
        self.aims = aims

    def properties_str(self):
        if self.properties is None:
            return ""
        return "\n".join(f"+ {prop}" for prop in self.properties)

    def description(self):
        fields = []
        if self.id is not None:
            fields.append(self.id)
        if self.properties is not None:
            fields.append(self.properties_str())
        if self.contents is not None:
            fields.append(f"Inhalte:\n{self.contents}")
        if self.aims is not None:
            fields.append(f"Ziele:\n{self.aims}")
        return "\n\n".join(fields)

    def href_title(self):
        if self.url is None:
            return self.title
        return f"[{self.title}]({self.url})"

    def embed(self):
        emb = {
            "author": self.lecturer.json(),
            "title": self.title,
            "description": self.description()
        }
        if self.color is not None:
            emb["color"] = int(self.color)
        if self.url is not None:
            emb["url"] = self.url
        return emb

    @staticmethod
    def from_json(json_obj, lecturers: dict[Lecturer]) -> Module:
        # find lecturer
        lecturer_id = json_get(json_obj, "lecturer")
        if lecturer_id not in lecturers:
            raise KeyError("Invalid Lecturer ID")
        lecturer = lecturers[lecturer_id]
        # get color
        color = json_get(json_obj, "color")
        if color is None:
            color = Module.standard_color

        return Module(title=json_get(json_obj, "title"),
                      lecturer=lecturer,
                      color=color,
                      id=json_get(json_obj, "id"),
                      url=json_get(json_obj, "url"),
                      properties=json_get(json_obj, "properties"),
                      contents=json_get(json_obj, "contents"),
                      aims=json_get(json_obj, "aims"))

    @staticmethod
    def from_json_arr(json_arr, lecturers: dict[Lecturer]) -> list[Module]:
        return [Module.from_json(json_obj, lecturers) for json_obj in json_arr]


def post(module: Module, webhook_url):
    res = requests.post(webhook_url, json={"embeds": [module.embed()]})
    if res.text:
        print(res.text)


def main():
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
        webhook_url = config["webhook_url"]
        Module.standard_color = config["embed_color"]

    with open(LECTURERS_PATH, "r") as f:
        lecturers = Lecturer.from_json_arr(json.load(f))
    with open(MODULES_PATH, "r") as f:
        modules = Module.from_json_arr(json.load(f), lecturers)

    for module in modules:
        post(module, webhook_url)
        sleep(1)


if __name__ == "__main__":
    main()
