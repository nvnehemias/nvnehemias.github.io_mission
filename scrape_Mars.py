# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

#mars_scrape_info = {}

def browser_start():
    #https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    #!which chromedriver
    executable_path = {'executable_path': '/Users/nehemias/Downloads/chromedriver'}
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)



# NASA Mars News
def scrape():

    browser = browser_start()
    mars_scrape_info = {}
    
    # URL of page to be scraped
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    #Visit website
    browser.visit(news_url)

    #Parse html with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Attain the div class and create a new empty list
    news_title = soup.find('div',class_ = "content_title").text


    #Attain the div class and create a new empty list
    news_p = soup.find('div',class_ = "article_teaser_body").text

    mars_scrape_info["news_title"] = news_title
    mars_scrape_info["news_paragraph"] = news_p


    # URL of page to be scraped
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    #Visit website
    browser.visit(image_url)

    #Parse html with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Attain article tags and image url
    new_result = soup.find_all('article')
    split_url = new_result[0].attrs['style'][23:-3]
    featured_image_url = f"https://www.jpl.nasa.gov{split_url}"
    
    
    mars_scrape_info["featured_image_url"] = featured_image_url


    # URL of page to be scraped
    weather_url = "https://twitter.com/marswxreport?lang=en"

    #Visit website
    browser.visit(weather_url)

    #Parse html with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Attain the p tags and class and print tweet
    mars_tweet = soup.find('p', class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_scrape_info["mars_weather"] = mars_tweet
    

    # URL of page to be scraped
    mars_facts_url = "https://space-facts.com/mars/"

    #Visit website
    browser.visit(mars_facts_url)

    #read html to pandas dataframe
    df = pd.read_html(mars_facts_url)

    #Dataframe  
    df1 = df[1]
    
    #Rename columns
    df1.columns = ["description","Value"]

    #Setting index
    df1.set_index("description", inplace = True)

    #Convert dataframe to html
    data = df1.to_html()

    data = data.replace("\n", "")

    mars_scrape_info["mars_facts"] = data

    # Mars Hemispheres


    # URL of page to be scraped
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    #Visit website
    browser.visit(hemispheres_url)

    #Parse html with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Attain the image and thumb class 
    new_images = soup.find_all("img",class_ = "thumb")

    #Empty list and names of hemispheres
    hemisphere_image_urls = []
    list_names = ["Cerberus Hemisphere","Schiaparelli Hemisphere","Syrtis Major Hemisphere","Valles Marineris Hemisphere"]

    #For loop to obtain complete url
    for i in range(len(new_images)):
        src_url = new_images[i].attrs["src"]
        dictionary = {"title": list_names[i],"image_url": f"https://astrogeology.usgs.gov{src_url}"}
        hemisphere_image_urls.append(dictionary)


    mars_scrape_info["hemisphere_image_urls"] = hemisphere_image_urls


    browser.quit()
    return mars_scrape_info
