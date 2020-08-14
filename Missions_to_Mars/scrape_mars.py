# Import dependicies
from bs4 import BeautifulSoup
from splinter import Browser
from pprint import pprint
import pymongo
import pandas as pd
import requests
import time
 

# Define browser
def init_browser():
    executable_path = {'executable_path': 'C:\\Users\\jtile\\Documents\\Python Scripts\\chromedriver'}
    # browser = Browser('chrome',**execpath,headless=False)
    return Browser('chrome', **executable_path, headless=False)

 
def scrape():
    
    browser = init_browser()
    mars_collection = {}
     
    # Get Mars news
    browser.visit("https://mars.nasa.gov/news")
    time.sleep(10)
  
    soup = BeautifulSoup(browser.html, 'html.parser')
    
    # Get news title
    mars_collection["news_title"] = soup.find_all("div",class_="content_title")[1].get_text()
   

    # Get news paragraph
    mars_collection["news_p"] = soup.find_all("div",class_="article_teaser_body")[0].get_text()
   

    # Get featured image
    #browser = Browser('chrome',**execpath,headless=False)
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    time.sleep(10)
    url = ('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # pull images from website
    images = soup.find_all('a', class_="fancybox")
    
    # pull image link
    pic_src = []
    for image in images:
        pic = image['data-fancybox-href']
        pic_src.append(pic)

    mars_collection["featured_image_url"] = 'https://www.jpl.nasa.gov' + pic
    

    # Mars weather
    #browser = Browser('chrome',**execpath,headless=False)
    browser.visit('https://twitter.com/marswxreport?lang=en')
    time.sleep(10)
    soup = BeautifulSoup(browser.html, 'html.parser')

    
    contents = soup.find_all("div",class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    mars_collection["mars_weather"] = contents[0].get_text()

    # Get Mars facts from Mars Facts webpage.
    browser.visit("https://space-facts.com/mars/")
    time.sleep(10)

    soup = BeautifulSoup(browser.html, 'html.parser')
    
    url = r'https://space-facts.com/mars/'
    tables = pd.read_html(url) # Returns list of all tables on page
   
    mars_collection["mars_table"] = tables[0].to_html() # Select table of interest
   

    # Get image links from Mars Hemisphere

    browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    time.sleep(10)

    hemisphere_image_urls = []

    soup = BeautifulSoup(browser.html, 'html.parser')
    print(soup.prettify())

    # Get titles and links from main Mars Hemispheres page
    image_data = soup.find_all('a', class_="itemLink product-item")
    url_list = []
    title_list = []
    counter = 0

    for i in image_data:
        counter+=1
        if i.get_text():
            url_list.append(i.get('href'))
            title_list.append(i.get_text())
        
    
    # *** Test ****
    # loop thru url_list and get image from each page
    # https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced

    astro_link = (f'https://astrogeology.usgs.gov/{url_list[0]}')

    browser.visit(astro_link)
    time.sleep(10)

    soup = BeautifulSoup(browser.html, 'html.parser')
    print(soup.prettify())

    pic = soup.find('li')
    img_link = pic.find('a')['href']
    print(img_link)

    # loop thru url_list and get image from each page
    # https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced

    img_link = []
    for a in url_list:
        astro_link = (f'https://astrogeology.usgs.gov/{a}')
#   print(astro_link)

        browser.visit(astro_link)
        time.sleep(10)

        soup = BeautifulSoup(browser.html, 'html.parser')
    
        pic = soup.find('li')
        img_link.append(pic.find('a')['href'])
    
#    for t in title_list:
#        print(t)

    # Build dictionary
    hemisphere_image_urls = []
    for (t,i) in zip(title_list, img_link):
        data_dict = dict({'title':t, 'img_url':i})
        hemisphere_image_urls.append(data_dict)

    mars_collection["hemisphere_image"] = hemisphere_image_urls

    # close browser
    browser.quit()

    return mars_collection
