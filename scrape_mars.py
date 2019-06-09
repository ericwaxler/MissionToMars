from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)

    #scrape news data

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    print(news_title)
    print(news_p)

    #scrape featured image

    url = 'https://www.jpl.nasa.gov'
    mars_uri = '/spaceimages/?search=&category=Mars'
    browser.visit(url + mars_uri)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = url + soup.find('a', class_='button fancybox')['data-fancybox-href']

    print(featured_image_url)

    #scrape weather

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('p', class_='tweet-text', text=True).text

    print(mars_weather)

    #scrape facts

    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    fact_table = pd.read_html(url)
    html_table = fact_table[0].to_html()
    print(html_table)

    #scrape hemisphere images

    url = 'https://astrogeology.usgs.gov'
    uri = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url + uri)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_='item')

    titles = []
    image_page_list = []
    image_url_list = []
    hemisphere_image_urls = []


    for item in items:
        print(item.find('h3').text[0:-9])
        titles.append(item.find('h3').text[0:-9])
        print(item.find('a', class_='itemLink')['href'])
        image_page_list.append(url + item.find('a', class_='itemLink')['href'])

        browser.click_link_by_partial_text('Hemisphere')
        time.sleep(1)
        print(BeautifulSoup(browser.html, 'html.parser').find('li').find('a')['href'])
        image_url_list.append(BeautifulSoup(browser.html, 'html.parser').find('li').find('a')['href'])

    for i in range(len(titles)):
        hemisphere_image_urls.append({'title':titles[i],'img_url':image_url_list[i]})

    browser.quit()

    #construct dictionary
    mars_data = {
        'news_title': news_title,
        'news_para': news_p,
        'feat_img': featured_image_url,
        'weather': mars_weather,
        'facts': html_table,
        'hemi_urls': hemisphere_image_urls
    }

    return mars_data
