import pandas as pd # The pandas library for data analysis and manipulation.
import requests as requests # Requests for making network connections.
from bs4 import BeautifulSoup # For extracting data from HTML and XML docs.
import time


def user_selection():
    '''Allows the user to choose the next selection based on a single integer'''
    print("\n\nChoose the next selection: ")
    print("1: Sort shops")
    print("2: List shop's popular items")
    print("3: Search another city")
    print("4: Export results to file")
    print("5: Exit")
    option = input("Option: ")
    return int(option)

    


def user_input(option):
    ''''Allows the user to write out the city or sorting method'''
    if(option == "city"):
        selection = input("Type a city in California to search for Tea Shops in or type 'None': ")
        return selection
    elif(option == "sort"):
        selection = input("Would you like to sort by 'Highest Rated' or 'Most Reviewed': ")
        return selection

def build_url(location):
    '''Builds the Yelp URL based on the city decided'''
    string_location = ""
    if(len(location.split()) > 1):
        split_location = location.split()
        string_location = "+".join(split_location)
    else:
        string_location = location
    
    url_location = "https://www.yelp.com/search?find_desc=tea&find_loc=" + string_location +"%2C+CA"
    return url_location



def export_results(raw_data):
    '''Uses the data created to add it to a dataframe'''
    dataframe = pd.DataFrame(raw_data, columns = ['Store', 'Rating', 'Reviews'])
    dataframe.index += 1
    print(dataframe)
    return dataframe


def store_data(beautifulsoup):
    '''Search through the tags of the tea shops from a certain city and store the data into a dictionary'''
    names = []
    urls = []
    ratings = []
    reviews = []
    for store in beautifulsoup.find_all('li', 'css-1qn0b6x'):
        name = store.find('a', 'css-19v1rkv')
        rating = store.find('span', 'css-gutk1c')
        review = store.find('span', 'css-chan6m')
        if(name != None):
            urls.append(("https://www.yelp.com"+name.get('href')))
            names.append(name.get_text())
            ratings.append(rating.get_text())
            reviews.append(review.get_text())
    raw_data={
        'Store':names,
        'Rating':ratings,
        'Reviews':reviews,
        'URLS': urls
    }
    return raw_data


def sort_highest_rated(dataframe):
    '''Sort stores by the highest ratings and display results'''
    # print(dataframe.Rating.to_string(index=False))
    dataframe = dataframe.sort_values(by='Rating', ascending=False)
    dataframe = dataframe.reset_index(drop=True)
    dataframe.index += 1
    print(dataframe)


def sort_most_reviewed(dataframe):
    '''Sort stores by the most reviewed and display results'''
    size = dataframe[dataframe.columns[0]].count()
    # print(dataframe)
    for i in range(size):
        value = dataframe.iloc[i, 2]
        string_value = (value.split()[0])[1:]
        dataframe.iloc[i, 2] = string_value
    dataframe.Reviews =  (dataframe.Reviews.replace(r'[kKmM]+$', '', regex=True).astype(float) * \
        dataframe.Reviews.str.extract(r'[\d\.]+([kKmM]+)', expand=False)
        .fillna(1)
        .replace(['k','m'], [10**3, 10**6]).astype(int))
    dataframe = dataframe.sort_values(by = "Reviews", ascending=False)
    dataframe = dataframe.reset_index(drop=True)
    for i in range(size):
        value = dataframe.iloc[i, 2]
        # string_value = (value.split()[0])[1:]
        dataframe.iloc[i, 2] = "(" + str(int(value)) + " reviews)"
    dataframe.index += 1
    print(dataframe)



def store_popular_items(raw_data, dataframe):
    '''Search for store's popular items and display results'''
    export_results(raw_data)
    store_number = int(input("Select Store Number: "))
    print("\n", dataframe.iloc[[store_number-1]])
    store_url = raw_data['URLS'][store_number-1]
    print("Retrieving List... ")
    fetched_url = requests.get(store_url)
    beautifulsoup = BeautifulSoup(fetched_url.text, "html.parser")
    time.sleep(5)
    print("\nPopular Items: ")
    counter = 1
    for item in beautifulsoup.find_all('p', 'css-nyjpex'):
        print(str(counter)+ ":", item.get_text())
        counter += 1


def search_city_html():
    '''Retrieve user input of city selected and create a beautiful object from it'''
    location = user_input("city")
    fetched_url = requests.get(build_url(location))
    beautifulsoup = BeautifulSoup(fetched_url.text, "html.parser")
    return beautifulsoup
    




def shop_search():
    '''Main function that interacts with the user to retrieve their selection and return the results'''
    raw_data = {}
    dataframe = pd.DataFrame()
    selection = 3

    while(selection < 5):
        if(selection == 1):
            filter = user_input("sort")
            if(filter.strip() == "Highest Rated"):
                '''Highest Rated allows the user to see the stores ranked with highest ratings first'''
                sort_highest_rated(dataframe)

            elif(filter == "Most Reviewed"):
                '''Most Reviewed allows the user to see the stores ranked with highest reviews first'''
                sort_most_reviewed(dataframe)

        elif(selection == 2):
            '''Selection 2 allows the user to display the popular items from desired store'''
            store_popular_items(raw_data, dataframe)

        elif(selection == 3):
            '''Selection 3 allows the user to search for another city''' 
            beautifulsoup = search_city_html()
            raw_data = store_data(beautifulsoup)
            dataframe = export_results(raw_data)
        else:
            dataframe.to_csv('Tea_Shop_List.csv', index=False)
            print("Exported!")
        selection = user_selection()
    print("Goodbye!")



if __name__ == "__main__":
    shop_search()


