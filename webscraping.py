import pandas as pd # The pandas library for data analysis and manipulation.
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



if __name__ == "__main__":
    location = input("What location do you want to search for Tea Shops?: ")
    while(location != "None"):
        string_location = ""
        if(len(location.split()) > 1):
            split_location = location.split()
            string_location = "+".join(split_location)
        else:
            string_location = location
        # print(string_location)
        url_location = "https://www.yelp.com/search?find_desc=tea&find_loc=" + string_location +"%2C+CA"
        # print(url_location)
        fetched_url = requests.get(url_location)
        beautifulsoup = BeautifulSoup(fetched_url.text, "html.parser")
        counter = 1
        print("Top Results:")
        for shop in beautifulsoup.find_all('a', 'css-19v1rkv'):
            name = shop.string #shop name
            if( name != "Yelp" and name != "Food"):
                print(counter, ": ", name)
                counter += 1
        location = input("What location do you want to search for Tea Shops?: ")
