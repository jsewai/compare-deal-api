import re
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from rest_framework.response import Response
from rest_framework.decorators import api_view
from urllib.parse import quote
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_CRAGSLIST_URL = "https://toronto.craigslist.org/search/sss?query={}"
BASE_KIJIJI_URL = "https://www.kijiji.ca/b-city-of-toronto/{}/k0l1700273"

@api_view(['GET'])
def google(request):
    keyword = request.GET.get('search','baseball bat')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    safe_keyword = quote(keyword)
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.google.com/search?q={safe_keyword}&gl=ca&tbm=shop")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    dom = etree.HTML(str(soup))
    driver.quit()
    container = dom.xpath('/html/body/div/div/div[4]/div[3]/div/div[3]/div/div[2]/div')[0]
    cards = container.xpath('div[2]/following-sibling::div[position() <= 46]')
    ads_result = []
    for card in cards:
        ads_img = card.xpath('div//img')[0].get('src', '')
        ads_title = card.xpath('div//h3')[0].text
        ads_price = card.xpath('div//a/div/div[2]/span/span/span[1]/span')[0].text
        ads_url = "https://www.google.com" + card.xpath('div/div/span/a')[0].get('href', '')
        ads_result.append({'title': ads_title, 'ads_url': ads_url, 'price': ads_price, 'img_url': ads_img})
    counter =  '{} results by Google   '.format(len(ads_result))
    result_to_frontend = {
        'search': keyword,
        'ads_result': ads_result,
        'i': counter,
    }
    return Response(result_to_frontend)

@api_view(['GET'])
def kijiji(request):
    keyword = request.GET.get('search')
    final_search = BASE_KIJIJI_URL.format(quote_plus(keyword))
    print("final search is ", final_search)
    response = requests.get(final_search)  # sending request by using requests method
    data = response.text
    soup = BeautifulSoup(data, features="html.parser")
    data_listing = soup.find_all('li', attrs={'data-testid': re.compile(r'listing-card-list-item-\d+')})
    ads_result = []
    i = 0

    for attr in data_listing:
        ads_title = attr.find('h3', attrs={'data-testid': 'listing-title'})
        ads_url = ads_title.a["href"]
        post_url = "https://www.kijiji.ca{}".format(ads_url)
        post_title = ads_title.text.replace('\n', '')
        get_price = attr.find('p', attrs={'data-testid':'listing-price'})
        get_img = attr.find('img', attrs={'data-testid':'listing-card-image'})
        if get_price:
            post_price = get_price.text.replace('\n', '')
        else:
            post_price = 'N/A'

        # if attr.find('div', class_='image').find('img').get('data-src'):
        if get_img:
            # post_image = attr.find('img', attrs={'data-testid':'listing-card-image'}).get('src')
            post_image = get_img.get('src')
        else:
            post_image = "https://image-not-available.s3.us-east-2.amazonaws.com/image-not-available.png"
        ads_result.append({'title': post_title, 'ads_url': post_url, 'price': post_price, 'img_url': post_image})
        i += 1
    i = '{} results by Kijiji   '.format(i)
    result_to_frontend = {
        'search': keyword,
        'ads_result': ads_result,
        'i': i,
    }
    return Response(result_to_frontend)
