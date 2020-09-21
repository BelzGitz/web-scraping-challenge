#import dependencies

from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

#scrap websites for Mars data to be returned in a dictionary and dictonary
def scrape_mars():
    browser = init_browser()
    mars_data = {}

    #connect to a NASA website url
    url = 'http://mars.nasa.gov/news/'
    browser.visit(url)
    #create beautiful soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #scrape title and paragraph 
    news_title = soup.find("div",class_='list_text').find("div",class_='content_title').find("a").text
    news_p= soup.find("div",class_='article_teaser_body').text
    mars_data["news_title"]=news_title
    mars_data["news_p"]=news_p

    #connect url for Mars space image
    urlA="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(urlA)
    #scrape full size image 
    browser.click_link_by_id("full_image")
    browser.links.find_by_partial_text('more info')
    #create beautiful soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #locate large mars picture
    big_pic = soup.find("img",class_="fancybox-image")["src"]
    # define the base url
    base_url = "https://www.jpl.nasa.gov"
    #define full image url
    featured_image_url = base_url + big_pic
    mars_data["featured_image_url"] = featured_image_url

    #connect to url for mars facts url and use pandas to display mars facts on table 
    mars_facts_url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(mars_facts_url)
    mars_facts
    #Transform to panda DataFrame
    tables = pd.read_html(mars_facts_url)[0]
    #Assign columns
    tables.columns = ["Description","Value"]
    tables.set_index("Description", inplace=True)
    tables
    #save table to htlm
    tables_html = tables.to_html(justify = "left")
    mars_data["tables"]=tables_html

    #connect to url for Mars Hemisphere images
    mars_hem_url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hem_url)
    #create beautiful soup object
    html = browser.html
    hem_soup = BeautifulSoup(html, 'html.parser')
    #mars image hemispheres
    mars_hemispheres =["Cerberus","Schiaparelli","Syrtis Major","Valles Marineris"]
    hemisphere_image_urls = []
    #loop through images
    for hemisphere in mars_hemispheres:
        browser.click_link_by_partial_text(hemisphere)
        html = browser.html
        hem_soup = BeautifulSoup(html, 'html.parser')
        title = hem_soup.find("h2",class_='title').text
        img_url = hem_soup.find("li").a["href"]
        hemisphere_image_urls.append({"title":title, "img_url":img_url})
        hemisphere_image_urls
        browser.back()
        mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    #return dictionary
    return mars_data

if __name__ == "__main__":
    result = scrape_mars()
   # print(result)