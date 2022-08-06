import difflib
from bs4 import BeautifulSoup as bs
import requests
import dictlib
from pydash import merge_with

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
    
    def anime_go_and_zoro_to(self, name):
        zoro, zoro_img = self.zoroto(name)
        anigo, anigo_img = self.animego(name)
        merged = {}
        merged_img = {}
        for item in zoro.keys():
            merged[item] = [zoro[item]]
            merged_img[item] = [zoro_img[item]]
        for item in anigo.keys():
            try:
                merged[item] = [anigo[item], *merged[item]]
                merged_img[item] = [anigo_img[item], *merged_img[item]]
            except KeyError:
                merged[item] = [anigo[item]]
                merged_img[item] = [anigo_img[item]]
        merged = dict(sorted(merged.items()))
        merged_img = dict(sorted(merged_img.items()))
        return merged, merged_img
            