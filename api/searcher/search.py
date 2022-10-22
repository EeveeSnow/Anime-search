from pprint import pprint
import json
from bs4 import BeautifulSoup as bs
import requests

class Search_Long():
    # def anilist(self, name: str):
    #     query = '''
    #     query ($name: String) { # Define which variables will be used in the query (id)
    #     Media (search: $name, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
    #     idMal
    #     description
    #     bannerImage
    #     tags {
    #         name
    #     }
    #         title {
    #             romaji
    #             english
    #             native
    #         }
    #     }
    #     }
    #     '''

    #     variables = {
    #     'name': name
    #     }
    #     url = 'https://graphql.anilist.co'

    #     response = requests.post(url, json={'query': query, 'variables': variables})
    #     if response.ok:
    #         response = response.json()['data']['Media']
    #         tags = response["tags"][0:5]
    #         jp_name = response["title"]["native"]
    #         idM = response['idMal']
    #         description = response['description']
    #         bannerImage = response['bannerImage']
    #         return idM, jp_name, tags, description, bannerImage
    #     return None, None, None, None, None

    # def zoroto(self, name: str):

    #     params_zoro = {
    #     "keyword": name, 
    #     # "type": types_zoro[type_anime]
    #     }

    #     out = {}
    #     out_img = {}

    #     # going to zoro.to
    #     soup_zoro = bs(requests.get("https://zoro.to/search", params=params_zoro).text, "html.parser")
    #     anime_name_zoro = soup_zoro.findAll('h3', class_='film-name')
    #     anime_img = soup_zoro.find_all('div', class_='film-poster')
    #     for i in range(len(anime_name_zoro)):
    #         try:
    #             out[anime_name_zoro[i].a["title"]] = "https://zoro.to/watch" + anime_name_zoro[i].a["href"]
    #             out_img[anime_name_zoro[i].a["title"]] = anime_img[i].img["data-src"]
    #         except AttributeError:
    #             pass
    #     return out, out_img

    def animego(self, name: str):
        out = {}
        out_img = dict()
        if name == "":
            soup_animego = bs(requests.get("https://animego.org/anime?sort=a.title&direction=asc").text, "html.parser")
            anime_link_animego = soup_animego.findAll('div', class_="h5 font-weight-normal mb-1")
            anime_name_animego = soup_animego.findAll('div', class_='text-gray-dark-6 small mb-2')
            anime_img_animego = soup_animego.findAll('div', class_='anime-list-lazy lazy')
        else:
            params_animego = {
            "type": "small",
            "q": name
            }
            soup_animego = bs(requests.get("https://animego.org/search/anime",
             params=params_animego).text,"html.parser")
            anime_link_animego = soup_animego.findAll('div',
             class_='h5 font-weight-normal mb-2 card-title text-truncate')
            anime_name_animego = soup_animego.findAll('div', class_='text-gray-dark-6 small mb-1 d-none d-sm-block')
            anime_img_animego = soup_animego.findAll('div', class_='anime-grid-lazy lazy')
        for i in range(len(anime_link_animego)):
            try:
                out[anime_name_animego[i].text] = anime_link_animego[i].a["href"]
                out_img[anime_name_animego[i].text] = anime_img_animego[i]["data-original"]
            except AttributeError:
                pass
        return out, out_img


    def CardboardBoxWallpaper(self, item, title, out_wallpaper):
        '''Take item["images"] as item'''
        for img in item:
            if img["type"] == "wallpaper" and (img["height"] == 1080 and img["width"] == 1920):
                out_wallpaper[title] = [img["source"]]
                return(out_wallpaper)
        return(out_wallpaper)


    def CardboardBoxImg(self, item, title, out_img):
        '''Take item["images"] as item'''
        for img in item:
            if (img["width"] >= 200 and img["height"] >= 150 and img["width"] <= 1080 and img["height"] <= 1920) and\
                 (img["type"] == "poster" or img["type"] == "other"):
                out_img[title] = [img["source"]]
                return(out_img)
        return(out_img)


    def CardboardBoxSup(self, cardboard_data, out, out_img, out_wallpaper) :
        for item in cardboard_data:
            if item["platformId"] == "crunchyroll":
                try:
                    out[item["title"]] = [item["link"], *out[item["title"]]]
                except KeyError:
                    out[item["title"]] = [item["link"]]
                out_img = self.CardboardBoxImg(item["images"], item["title"], out_img)
                out_wallpaper = self.CardboardBoxWallpaper(item["images"], item["title"], out_wallpaper)
            elif item["platformId"] == "funimation" or item["platformId"] == "hidive":
                try: 
                    out[item["title"]] = [item["link"], *out[item["title"]]]
                except KeyError:
                    out[item["title"]] = [item["link"]]
                    out_img = self.CardboardBoxImg(item["images"], item["title"], out_img)
                    out_wallpaper = self.CardboardBoxWallpaper(item["images"], item["title"], out_wallpaper)
            if item["otherPlatforms"] != []:
                out, out_img, out_wallpaper = self.CardboardBoxSup(item["otherPlatforms"], out, out_img, out_wallpaper)
        return out, out_img, out_wallpaper


    def CardboardBox(self, name: str):
        params_cardboard = {"page":1, "size":50,"asc": True,"search":name,"queryables":{},"mature":0}

        out = {}
        out_img = {}
        out_wallpaper = {}

        cardboard_data = requests.post("https://cba-api.index-0.com/anime", json=params_cardboard, verify=False).json()
        out, out_img, out_wallpaper = self.CardboardBoxSup(cardboard_data["results"], out, out_img, out_wallpaper)
        return out, out_img, out_wallpaper

    # def wakanim(self, name):
    #     params_wakanim = {
    #         "search": name,
    #         "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJXZWJzaXRlSWQiOiIwIiwiTGFuZ3VhZ2VJZCI6IjAiLCJDb3VudHJ5IjoiRlIiLCJMYW5ndWFnZSI6ImZyIiwiaXNzIjoid2FrYW5pbS50diIsImF1ZCI6Indha2FuaW0udHYiLCJleHAiOjE2NjAwNTc1OTIsIm5iZiI6MTY1OTg4NDc4Mn0.Lnm3R6Q-97VCRCuH2448yMqDxTDyG4XWp6Jt3MHw4R8"
    #     }

    #     out = {}
    #     out_img = {}

    #     wakanim_data = requests.get("https://apiwaka.azure-api.net/search/v2/", params=params_wakanim).json()
    #     for item in wakanim_data["value"]:
    #         out[item["Name"]] = "https://www.wakanim.tv/fr/v2/catalogue/show/" + item["IdShowItem"]
    #         out_img[item["Name"]] = json.dumps(item["Image"])
    #     return out, out_img

    
    def all(self, name: str):
        # zoro, zoro_img = self.zoroto(name)
        anigo, anigo_img = self.animego(name)
        cardboard, cardboard_img, cardboard_wallpaper = self.CardboardBox(name)
        # wakanim, wakanim_img = self.wakanim(name)
        merged = {}
        merged_img = {}
        special_inf = {}
        for item in cardboard.keys():
            merged[item] = cardboard[item]
            merged_img[item] = cardboard_img[item]
        # for item in wakanim.keys():
        #     try:
        #         merged[item] = [wakanim[item], *merged[item]]
        #     except KeyError:
        #         merged[item] = [wakanim[item]]
        #         merged_img[item] = [wakanim_img[item]]
        for item in anigo.keys():
            try:
                merged[item] = [anigo[item], *merged[item]]
            except KeyError:
                merged[item] = [anigo[item]]
                merged_img[item] = [anigo_img[item]]
        # for item in zoro.keys():
        #     try:
        #         merged[item] = [zoro[item], *merged[item]]
        #     except KeyError:
        #         merged[item] = [zoro[item]]
        #         merged_img[item] = [zoro_img[item]]
        # merged = dict(sorted(merged.items()))
        # merged_img = dict(sorted(merged_img.items()))
        return merged, merged_img, cardboard_wallpaper
            
# test = Search_Long()
# pprint(test.CardboardBox("One Piece"))