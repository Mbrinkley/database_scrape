from bs4 import BeautifulSoup
from splinter import Browser
from pprint import pprint
import pymongo
import pandas as pd
import requests
from flask import Flask, render_template
import time
import numpy as np
import json
from selenium import webdriver

executable_path = {"executable_path": "/Users/16123/Desktop/chromedrv/chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)

url = "https://mars.nasa.gov/news/"
response = requests.get(url)
soup = bs(response.text, 'html.parser')

title = soup.find('div', class_="content_title").text
body= soup.find('div', class_="rollover_description").text

news_title = "Why This Martian Full Moon Looks Like Candy"
news_p = "For the first time, NASA's Mars Odyssey orbiter has caught the Martian moon Phobos during a full moon phase. Each color in this new image represents a temperature range detected by Odyssey's infrared camera."

# img 
img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
response = requests.get(img_url)
soup = bs(response.text, 'html.parser')

#scrape img 
#img link 
img = soup.find("a", class_="fancybox")
featured_image_url = "https://jpl.nasa.gov/spaceimages/images/mediumsize/PIA17009_ip.jpg"

#Mars weather twitter account
weather_url = "https://twitter.com/marswxreport?lang=en"
response = requests.get(weather_url)
soup = bs(response.text, 'html.parser')
#scrape twitter 
tweet = soup.find("div", class_="content").text
mars_weather = "InSight sol 167 (2019-05-17) low -100.5ºC (-148.9ºF) high -20.4ºC (-4.6ºF) winds from the SW at 4.7 m/s (10.6 mph) gusting to 13.5 m/s (30.3 mph)"
#mars facts
facts_url = "https://space-facts.com/mars/"
response = requests.get(facts_url)
soup = bs(response.text, 'html.parser')

#turn facts into html table string
mars_table = pd.read_html(facts_url)
mars_table[0]
mars_df = mars_table[0]
mars_df.columns=["Facts", "Values"]
mars_table_html= mars_df.to_html()
mars_table_html = mars_table_html.replace("\n", "")

# Mars Hemispheres 
hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
response = requests.get(hemisphere_url)
soup = bs(response.text, 'html.parser')
hemisphere_image_urls = []
#scrape through the hemispheres and pull each image's url 
Cerberus_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced')
response = requests.get(Cerberus_url)
soup = bs(response.text, 'html.parser')

cerberus_img = soup.find('div', class_="wide-image-wrapper")
cerberus_pic = "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"

cerberus_title = soup.find('h2', class_="title").text
cerberus_hem = {"title": cerberus_title, "cerberus_img": cerberus_pic}

#Schiaparelli Hemisphere
schi_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced')

response = requests.get(schi_url)
soup = bs(response.text, 'html.parser')

schi_img = soup.find('div', class_="wide-image-wrapper")
schi_pic = "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"

Schiaparelli_title = soup.find('h2', class_="title").text
Schiaparelli_hem = {"title": Schiaparelli_title, "Schiaparelli_img": schi_pic}

#syrtis major hemisphere
syrtis_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced')

response = requests.get(syrtis_url)
soup = bs(response.text, 'html.parser')
syrtis_img = soup.find('div', class_="wide-image-wrapper")
syrtis_pic = "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"

syrtis_title = soup.find('h2', class_="title").text
syrtis_hem = {"title": syrtis_title, "syrtis_img": syrtis_pic}

#Valles Marineris Hemisphere 

valles_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced')

response = requests.get(valles_url)
soup = bs(response.text, 'html.parser')

valles_img = soup.find('div', class_="wide-image-wrapper")
valles_pic = "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"

valles_title = soup.find('h2', class_="title").text
valles_hem = {"title": valles_title, "valles_img": valles_pic}

hemisphere_image_urls = [cerberus_hem, Schiaparelli_hem, syrtis_hem, valles_hem]
#collection for mongodb
mars_collection["hemisphere_image"] = hemisphere_image_urls

return mars_collection
