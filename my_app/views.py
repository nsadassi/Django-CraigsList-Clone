from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = 'https://sfbay.craigslist.org/search/bbb?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    
    to_search_url = BASE_CRAIGSLIST_URL.format(quote_plus(search) )
    #print(to_search_url)
    response = requests.get(to_search_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class' : 'result-row'})
    #post_titles = post_listings[0].find(class_ = 'result-title').text
    #post_url = post_listings[0].find('a').get('href')
    #post_price = post_listings[0].find(class_='result-price').text

    #print(post_titles, post_url, post_price)

    final_postings = []

    for post in post_listings:
        post_titles = post.find(class_ = 'result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        
        #post_image_url='https://p4.wallpaperbetter.com/wallpaper/981/316/907/happoubi-jin-snyp-anime-girls-1920x1080-anime-hot-anime-hd-art-wallpaper-preview.jpg'
        if post.find(class_='result-image').get('data-ids'):
            post_image = post.find(class_='result-image').get('data-ids').split(',')[0]
            #print(post_image)
            post_image = post_image[2::]
            #print(post_image)
            post_image_url = BASE_IMAGE_URL.format(quote_plus(post_image))
            #print(post_image)
        else:
            post_image_url='https://p4.wallpaperbetter.com/wallpaper/981/316/907/happoubi-jin-snyp-anime-girls-1920x1080-anime-hot-anime-hd-art-wallpaper-preview.jpg'

        final_postings.append((post_titles, post_url, post_price, post_image_url))

    
    stuff_for_frontend = {
        'search_term' : search,
        'final_postings' : final_postings, 
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)