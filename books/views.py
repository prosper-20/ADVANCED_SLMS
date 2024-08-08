from django.shortcuts import render
import requests
from decouple import config

# id_list = []
# url = f"https://api.bigbookapi.com/search-books?query=signals-and-systems&min-rating=0.8&api-key={config('USER_TWO_BIG_BOOK_API_KEY')}"
# response = requests.get(url)
# data = response.json()
# for book_list in data['books']:
#     for book in book_list:
#         # Extract the id and append to id_list
#         id_list.append(book['id'])


# print(id_list)

def search_book(query):
    my_ids = []
    search_url = f"https://api.bigbookapi.com/search-books?query={query}&min-rating=0.8&api-key={config('USER_TWO_BIG_BOOK_API_KEY')}"
    response = requests.get(search_url)
    data = response.json()
    for book_list in data['books']:
        for book in book_list:
        # Extract the id and append to id_list
            my_ids.append(book['id'])
    return my_ids[:3] #display only the first three book ids




def full_book_details(book_ids):
    full_book_info = []
    for book_id in book_ids:
        full_book_url = f"https://api.bigbookapi.com/{book_id}?api-key={config('USER_TWO_BIG_BOOK_API_KEY')}"
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
