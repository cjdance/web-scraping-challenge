from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


def scrape():

    browser = init_browser()

    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    time.sleep(5)
    news_html = browser.html
    soup = bs(news_html,'html.parser')
    result = soup.find('div', class_="list_text")
    news_title = result.find("div", class_ = "content_title").text
    news_para = result.find('div',class_="article_teaser_body").text

    img_url = 'https://spaceimages-mars.com'
    browser.visit(img_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    img_html = browser.html
    soup = bs(img_html, "html.parser")
    image_url = soup.find_all("img")
    image_url = image_url[1]['src']
    featured_image_url = str(img_url) + '/' + str(image_url)

    facts_url = 'https://galaxyfacts-mars.com'
    browser.visit(facts_url)
    tables = pd.read_html(facts_url)
    mars_df = tables[0]
    mars_df.columns = ["Description","Values","Drop"]
    mars_df.set_index("Description", inplace=True)
    mars_df = mars_df.drop(axis=0, labels = 'Mars - Earth Comparison')
    mars_df = mars_df.drop(axis=1, labels = "Drop")
    html_table = mars_df.to_html()
    html_table.replace("\n", '')
    mars_df.to_html("mars_facts_data.html")

    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    html_hemi = browser.html
    soup = bs(html_hemi, "html.parser")
    hemispheres = soup.find_all("div", class_="item")

    hemispheres_info = []

    for i in hemispheres:
        title = i.find("h3").text
        hemispheres_img = i.find("a", class_="itemLink product-item")["href"]
    
    # Visit the link that contains the full image website 
        browser.visit(hemi_url + hemispheres_img)
    
    # HTML Object
        image_html = browser.html
        web_info = bs(image_html, "html.parser")
    
    # Create full image url
        img_url = hemi_url + web_info.find("img", class_="wide-image")["src"]
    
        hemispheres_info.append({"title" : title, "img_url" : img_url})

    mars_info = {
        "news-title": news_title,
        "news-paragraph": news_para,
        "featured_image": featured_image_url,
        "facts": mars_df,
        "hemispheres": hemispheres_info
    }
    browser.quit()

    return mars_info