from pprint import pprint
import json
from bs4 import BeautifulSoup as bs
import requests

class Search_Long():
    def zoroto(self, name: str):

        params_zoro = {
        "keyword": name, 
        # "type": types_zoro[type_anime]
        }

        out = {}
        out_img = {}

        # going to zoro.to
        soup_zoro = bs(requests.get("https://zoro.to/search", params=params_zoro).text, "html.parser")
        anime_name_zoro = soup_zoro.findAll('h3', class_='film-name')
        anime_img = soup_zoro.find_all('div', class_='film-poster')
        for i in range(len(anime_name_zoro)):
            try:
                out[anime_name_zoro[i].a["title"]] = "https://zoro.to/watch" + anime_name_zoro[i].a["href"]
                out_img[anime_name_zoro[i].a["title"]] = anime_img[i].img["data-src"]
            except AttributeError:
                pass
        return out, out_img

    def animego(self, name: str):

        params_animego = {
        "type": "small",
        "q": name}

        out = {}
        out_img = {}

        soup_animego = bs(requests.get("https://animego.org/search/anime", params=params_animego).text, "html.parser")
        anime_link_animego = soup_animego.findAll('div', class_='h5 font-weight-normal mb-2 card-title text-truncate')
        anime_name_animego = soup_animego.findAll('div', class_='text-gray-dark-6 small mb-1 d-none d-sm-block')
        anime_img_animego = soup_animego.findAll('div', class_='anime-grid-lazy lazy')
        for i in range(len(anime_link_animego)):
            try:
                out[anime_name_animego[i].text] = anime_link_animego[i].a["href"]
                out_img[anime_name_animego[i].text] = anime_img_animego[i]["data-original"]
            except AttributeError:
                pass
        return out, out_img

    def CardboardBox(self, name: str):

        params_cardboard = {"page":1, "size":50,"asc": True,"search":name,"queryables":{},"mature":0}

        out = {}
        out_img = {}

        cardboard_data = requests.post("https://cba-api.index-0.com/anime/v2", json=params_cardboard, verify=False).json()
        
        for item in cardboard_data["results"]:
            if item["platformId"] == "crunchyroll":
                try: 
                    out[item["title"]] = ["https://beta.crunchyroll.com/" + item["type"] + "/" + "animeId", *out[item["title"]]]
                    for img in item["images"]:
                        if (img["width"] >= 240 and img["height"] >= 360 and img["width"] <= 1080 and img["height"] <= 1980) and (img["type"] == "poster" or img["type"] == "other"):
                            out_img[item["title"]] = [img["source"]]
                            break
                except KeyError:
                    out[item["title"]] = ["https://beta.crunchyroll.com/" + item["type"] + "/" + "animeId"]
                    for img in item["images"]:
                        if (img["width"] >= 240 and img["height"] >= 360 and img["width"] <= 1080 and img["height"] <= 1980) and (img["type"] == "poster" or img["type"] == "other"):
                            out_img[item["title"]] = [img["source"]]
                            break
            elif item["platformId"] == "funimation":
                try: 
                    out[item["title"]] = [item["link"], *out[item["title"]]]
                except KeyError:
                    out[item["title"]] = [item["link"]]
                    for img in item["images"]:
                        if (img["width"] >= 240 and img["height"] >= 360 and img["width"] <= 1080 and img["height"] <= 1980) and (img["type"] == "poster" or img["type"] == "other"):
                            out_img[item["title"]] = [img["source"]]
                            break
            elif item["platformId"] == "hidive":
                try: 
                    out[item["title"]] = [item["link"], *out[item["title"]]]
                except KeyError:
                    out[item["title"]] = [item["link"]]
                    for img in item["images"]:
                        if (img["width"] >= 240 and img["width"] <= 1080 and img["height"] <= 1980) and (img["type"] == "poster" or img["type"] == "other"):
                            out_img[item["title"]] = [img["source"]]
                            break
        return out, out_img

    def wakanim(self, name):
        params_wakanim = {
            "search": name,
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJXZWJzaXRlSWQiOiIwIiwiTGFuZ3VhZ2VJZCI6IjAiLCJDb3VudHJ5IjoiRlIiLCJMYW5ndWFnZSI6ImZyIiwiaXNzIjoid2FrYW5pbS50diIsImF1ZCI6Indha2FuaW0udHYiLCJleHAiOjE2NjAwNTc1OTIsIm5iZiI6MTY1OTg4NDc4Mn0.Lnm3R6Q-97VCRCuH2448yMqDxTDyG4XWp6Jt3MHw4R8"
        }

        out = {}
        out_img = {}

        wakanim_data = requests.get("https://apiwaka.azure-api.net/search/v2/", params=params_wakanim).json()
        for item in wakanim_data["value"]:
            out[item["Name"]] = "https://www.wakanim.tv/fr/v2/catalogue/show/" + item["IdShowItem"]
            out_img[item["Name"]] = json.dumps(item["Image"])
        return out, out_img

    
    def all(self, name: str):
        zoro, zoro_img = self.zoroto(name)
        anigo, anigo_img = self.animego(name)
        carboard, carboard_img = self.CardboardBox(name)
        wakanim, wakanim_img = self.wakanim(name)
        merged = {}
        merged_img = {}
        for item in carboard.keys():
            merged[item] = carboard[item]
            merged_img[item] = carboard_img[item]
        for item in wakanim.keys():
            try:
                merged[item] = [wakanim[item], *merged[item]]
            except KeyError:
                merged[item] = [wakanim[item]]
                merged_img[item] = [wakanim_img[item]]
        for item in anigo.keys():
            try:
                merged[item] = [anigo[item], *merged[item]]
            except KeyError:
                merged[item] = [anigo[item]]
                merged_img[item] = [anigo_img[item]]
        for item in zoro.keys():
            try:
                merged[item] = [zoro[item], *merged[item]]
            except KeyError:
                merged[item] = [zoro[item]]
                merged_img[item] = [zoro_img[item]]
        # merged = dict(sorted(merged.items()))
        # merged_img = dict(sorted(merged_img.items()))
        return merged, merged_img
            
# test = Search_Long()
# pprint(test.CardboardBox("One Piece"))
