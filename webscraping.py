import pandas as pd # The pandas library for data analysis and manipulation.
import requests as requests # Requests for making network connections.
from bs4 import BeautifulSoup # For extracting data from HTML and XML docs.
from natsort import index_natsorted


def user_selection():
    print("\n\nChoose the next selection: ")
    print("1. Sort shops")
    print("2. List shop's popular items")
    print("3. Search another city")
    print("4: Exit")
    option = input("Option: ")
    return int(option)

    


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

def top_results(beautifulsoup):
    # fetched_url = requests.get(build_url(location))
    # beautifulsoup = BeautifulSoup(fetched_url.text, "html.parser")
    counter = 1
    print("Top Results:")
    for shop in beautifulsoup.find_all('a', 'css-19v1rkv'):
        name = shop.string #shop name
        if( name != "Yelp" and name != "Food"):
            print(counter, ": ", name)
            counter += 1

def export_results(raw_data):
    dataframe = pd.DataFrame(raw_data, columns = ['Store', 'Rating', 'Reviews'])
    dataframe.index += 1
    # dataframe.to_csv('raw_data.csv', index=False)
    print(dataframe)
    return dataframe


def store_data(beautifulsoup):
    names = []
    urls = []
    ratings = []
    reviews = []
    for store in beautifulsoup.find_all('li', 'css-1qn0b6x'):
        name = store.find('a', 'css-19v1rkv')
        rating = store.find('span', 'css-gutk1c')
        review = store.find('span', 'css-chan6m')
        if(name != None):
            names.append(name.get_text())
            ratings.append(rating.get_text())
            reviews.append(review.get_text())
    raw_data={
        'Store':names,
        'Rating':ratings,
        'Reviews':reviews
    }
    return raw_data
    


def shop_search():
    location = user_input("city")
    fetched_url = requests.get(build_url(location))
    beautifulsoup = BeautifulSoup(fetched_url.text, "html.parser")
    # top_results(beautifulsoup)
    raw_data = store_data(beautifulsoup)


    dataframe = export_results(raw_data)
    selection = user_selection()
    while(selection < 4):
        if(selection == 1):
            filter = user_input("sort")
            if(filter.strip() == "Highest Rated"):
                # print(dataframe.Rating.to_string(index=False))
                dataframe = dataframe.sort_values(by='Rating', ascending=False)
            elif(filter == "Most Reviewed"):
                # need to modify the sorting key
                # for r in dataframe['Store']:
                #     print(dataframe[r])
                size = dataframe[dataframe.columns[0]].count()
                # dataframe['Reviews'].replace({'K': '*1e3', 'M': '*1e6'}, regex=True).map(pd.eval).astype(int)
                print(dataframe)
                for i in range(size):
                    # (df.Val.replace(r'[KM]+$', '', regex=True).astype(float) * df.Val.str.extract(r'[\d\.]+([KM]+)', expand=False).fillna(1).replace(['K','M'], [10**3, 10**6]).astype(int))
                    
                    
                    value = dataframe.iloc[i, 2]
                    string_value = (value.split()[0])[1:]
                    # dataframe.iloc[i, 2] = string_value
                    # string_value.replace({'k': '*1e3', 'm': '*1e6'}, regex=True).map(pd.eval).astype(int)
                    print(string_value)
                print(dataframe.Reviews.to_string(index=False))
                dataframe['Reviews'].replace({'[kK]': '*1e3', 'm': '*1e6'}, regex=True)
           
            
            



                # dataframe.iloc[:, 2:] = 1
                # print(dataframe)
                # https://github.com/SethMMorton/natsort?tab=readme-ov-file#sorting-by-real-numbers-i-e-signed-floats
                # dataframe = dataframe.sort_values(by='Reviews', ascending=False, key=lambda x: np.argsort(index_natsorted(dataframe["Reviews"])))
                # dataframe = dataframe.sort_values(by = "Reviews", ascending=False)
                print(dataframe.Reviews.to_string(index=False))
            dataframe = dataframe.reset_index(drop=True)
            dataframe.index += 1
            print(dataframe)
        elif(selection == 2):
            print("listing popular items...")
        else:
            location = user_input("city")
            fetched_url = requests.get(build_url(location))
            # print(fetched_url)
            beautifulsoup = BeautifulSoup(fetched_url.text, "html.parser")
            raw_data = store_data(beautifulsoup)
            dataframe = export_results(raw_data)
            # top_results(beautifulsoup)
        selection = user_selection()
    
    print("Goodbye!")



if __name__ == "__main__":
    shop_search()


