# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import requests
from bs4 import BeautifulSoup


url = "http://www.lazada.co.id/beli-laptop/"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")


g_pages = soup.find_all("span", {"class" : "pages"})[0].find_all("a");
max_pages = int(g_pages[len(g_pages)-1].text)
page = 1
max_pages = 2
data = []
while page <= max_pages :
    r = requests.get(url+"?page="+str(page))
    soup = BeautifulSoup(r.content, "html.parser")
    g_data = soup.find_all("div",{"data-qa-locator":"product-item"})

    address= ""
    title = ""
    merek = ""
    tipe_produk = ""
    harga_net = ""
    long_spek = []
    rating = 0
    jml_ulasan = 0
    
    for item in g_data:
        link = item.find_all("a")[0]
        product_desc = link.find_all("div", {"class":"product-card__description"})[0]
        rating_tag = link.find_all("div", {"class":"product-card__rating"})[0]
        spek_tag = product_desc.find_all("div", {"class" : "product-card__describtion--full"})[0]
        address = link.get("href")
        title = product_desc.find_all("div", {"class":"product-card__name-wrap"})[0].find_all("span")[0].get("title")
        harga_net = product_desc.find_all("div", {"class" : "product-card__button-buy"})[0].get("data-final-price")    
        
        
        short_spek = []
        for spekitem in spek_tag.find_all("li"):
            short_spek.append(spekitem.text)
        try:
            rating = rating_tag.find_all("div", {"class":"product-card__rating__stars"})[0].get("title")
            jml_ulasan_all = rating_tag.find_all("span", {"class" : "rating__number"})[0].text
            jml_ulasan = jml_ulasan_all[jml_ulasan_all.index("(")+1:jml_ulasan_all.index("Ulasan")-1]
        except:
            rating = -1
            jml_ulasan = -1
            pass
        
        data.append({ 'site' :'lazada','address' : address,
        'title' : title,
        'harga_net' : harga_net,
        'short_spek' : short_spek,
        'rating' : rating,
        'jml_ulasan' : jml_ulasan})
        
    page = page+1
    
with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)