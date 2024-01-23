# import pandas as pd # The pandas library for data analysis and manipulation.
import requests as requests # Requests for making network connections.
from bs4 import BeautifulSoup # For extracting data from HTML and XML docs.

# web_url = "https://www.yelp.com/search?find_desc=Tea&find_loc=Irvine%2C+CA&start=0"
# fetched_page = requests.get(web_url)

# #print(fetched_page.text)
# beautifulsoup = BeautifulSoup(fetched_page.text, "html.parser")

# for shop in beautifulsoup.find_all('a', 'css-19v1rkv'):
#     name = shop.string #shop name
#     if( name != "Yelp" and name != "Food"):
#         print(name)

# for page in beautifulsoup.find_all('a', "pagination-link-component__09f24__JRiQO css-ahgoya"):
#     print(page.get("href"))

def user_selection():
    print("\n\nChoose the next selection: ")
    print("1. Sort shops")
    print("2. List shop's popular items")
    print("3. Search another city")
    print("4: Exit")
    return int(input("Option: "))
    


def user_input(option):
    if(option == "city"):
        selection = input("Type a city in California to search for Tea Shops in or type 'None': ")
        return selection
    elif(option == "sort"):
        selection = input("Would you like to sort by 'Highest Rated' or 'Most Reviewed': ")
        return selection

def build_url(location):
    string_location = ""
    if(len(location.split()) > 1):
        split_location = location.split()
        string_location = "+".join(split_location)
    else:
        string_location = location
    # print(string_location)
    url_location = "https://www.yelp.com/search?find_desc=tea&find_loc=" + string_location +"%2C+CA"
    return url_location

def top_results(location):
    fetched_url = requests.get(build_url(location))
    beautifulsoup = BeautifulSoup(fetched_url.text, "html.parser")
    counter = 1
    print("Top Results:")
    for shop in beautifulsoup.find_all('a', 'css-19v1rkv'):
        name = shop.string #shop name
        if( name != "Yelp" and name != "Food"):
            print(counter, ": ", name)
            counter += 1


if __name__ == "__main__":
    location = user_input("city")
    top_results(location)
    selection = user_selection()
    while(selection < 4):
        if(selection == 1):
            user_input("sort")
        elif(selection == 2):
            print("listing popular items...")
        else:
            location = user_input("city")
            top_results(location)
        selection = user_selection()
    print("Goodbye!")


