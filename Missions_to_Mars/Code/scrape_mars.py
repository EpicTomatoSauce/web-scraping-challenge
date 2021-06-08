# dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
import time

# def splinter
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

# create scrape function
mars_data = {}
def scrape():
    browser = init_browser()
    
    ################################################################
    ### Mars News ###
    
    #URL to be scraped
    mars_url = 'https://redplanetscience.com/'
    browser.visit(mars_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(3)
    # scraping for news articles
    news_container = soup.find('div', class_='col-md-12')
    # in the news_container variable, find_all on 'div' and class_ = 'content_title' and 'article_teaser'body'
    news_title = news_container.find_all('div', class_='content_title')
    news_summary = news_container.find_all('div', class_='article_teaser_body')
    news_title_clean = news_title[0].text.strip()
    news_summary_clean = news_summary[0].text.strip()
    
    # insert scraped news info into mars_data dictionary
    mars_data['news_title'] = news_title_clean
    mars_data['news_summary'] = news_summary_clean
    
    ################################################################
    ### JPL Mars Space Images ###
    
    #URL to be scraped
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(3)
    # search for featured image class
    image_url = soup.find_all('a', class_='showimg')
    # find the href tag in the above class
    for image in image_url:
        featured_image_url_link = image['href']

    featured_image_url_link
    # get full url of image link
    featured_image_url = 'https://spaceimages-mars.com/' + featured_image_url_link
    featured_image_url
    
    # insert scraped featured photo into mars_data dictionary
    mars_data['featured_photo'] = featured_image_url
    
    ################################################################
    ### Mars Facts ###
    #URL to be scraped
    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(3)
    mars_table = pd.read_html(facts_url)
    mars_earth_comparison_table = mars_table[0]
    mars_table_facts = mars_table[1]
    mars_table_facts
    # change column names and strip ':' from first column
    mars_table_facts.columns = ['Statistic','Measurement']
    mars_table_facts['Statistic'] = mars_table_facts['Statistic'].str.strip(':')
    mars_table_facts = mars_table_facts.set_index('Statistic')
    mars_table_facts
    # convert to html and replace new lines with ''
    mars_html_table = mars_table_facts.to_html()
    mars_html_table.replace('\n', '')
    
    # insert scraped table into mars_data dictionary
    mars_data['mars_facts'] = mars_html_table
    
    ################################################################
    ### Mars Hemisphers ###
    #URL to be scraped
    mars_hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(mars_hemispheres_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(3)
    # initial scrape result in # result being found in html list. Need to search in result-list class first and then find 'a' tags contained in that.
    results_list = soup.find('div', class_ = 'result-list')
    field_item = results_list.find_all('a', class_ = 'itemLink product-item')
    # create a list of the hrefs
    hrefs_list = [item.get('href') for item in field_item]
    hrefs_list = list(set(hrefs_list))
    
    hemisphere_image_urls=[]
    for href in hrefs_list:
        target_url = mars_hemispheres_url + href
        browser.visit(target_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        time.sleep(3)

        # get title
        img_title = soup.find_all('h2', class_ = 'title')
        for title in img_title:
            img_title_clean = title.text.strip()

        # get image
        img_target = soup.find('div', class_ = 'downloads')
        img_url = img_target.find_all('a')[0]['href']

        # append to required list, note that base URL will have to be added to img_url to obtain full link
        hemisphere_image_urls.append({'title': img_title_clean, 'img_url': mars_hemispheres_url + img_url})
    
    # insert scraped image url list to mars_data
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls
    
    ################################################################
    
    browser.quit()
    
    return mars_data

scrape()
print(mars_data)
    
    
    