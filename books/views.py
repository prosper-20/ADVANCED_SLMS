from django.shortcuts import render
import requests
from decouple import config


# url = f"https://api.bigbookapi.com/search-books?query=software-development-techniques&min-rating=0.8&api-key={config('BIG_BOOK_API_KEY')}"
# response = requests.get(url)
# data = response.json()
# print(data)

def search_book(query):
    my_ids = []
    search_url = f"https://api.bigbookapi.com/search-books?query={query}&min-rating=0.8&api-key={config('BIG_BOOK_API_KEY')}"
    response = requests.get(search_url)
    data = response.json()
    ids = [book['id'] for book in data['books'][:3]]
    print('ids', ids)
    my_ids.extend(ids)
    print(my_ids)
    return my_ids #display only the first three book ids




def full_book_details(book_ids):
    full_book_info = []
    for book_id in book_ids:
        full_book_url = f"https://api.bigbookapi.com/{book_id}?api-key={config('BIG_BOOK_API_KEY')}"
        response = requests.get(full_book_url)
        full_book_info.append(response.json())
    # return full_book_info
    extracted_info = [
    {
        'title': book['title'],
        'image': book['image'],
        'authors': [author['name'] for author in book['authors']]
    }
    for book in full_book_info
]
    print(extracted_info)
    return extracted_info


# print(full_book_details([24258432, 23128316, 24434830, 15526320]))
