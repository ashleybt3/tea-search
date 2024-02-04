from webscraping import *
import pandas as pd
import requests as requests
from bs4 import BeautifulSoup
# import beavis

def test_sort_rating():
    ''''''

def test_sort_review():
    ''''''

def test_popular_items():
    ''''''

def test_search_city():
    df = pd.DataFrame({"Store": ["Mirakuru - The Miracle of Coffee & Tea", "Yellow Goose Cafe", "Moozi Tea Bar", "Airoma Cafe", "Sojeata", 
    "Phin Smith", "Tira Tea House", "KuteKook", "Summerfield Tea Bar", "Da Vien Coffee", ], "Rating": ["4.3", "4.3", "4.1", "4.7",
    "4.7", "4.8", "4.7", "4.5", "4.0","4.6"], "Reviews": ["(176 reviews)", "(67 reviews)", "(212 reviews)", "(860 reviews)", "(190 reviews)", 
    "(111 reviews)", "(435 reviews)", "(271 reviews)", "(522 reviews)",  "(1.8k reviews)"]})
    fetched_url = requests.get(build_url("Garden Grove"))
    beautifulsoup = BeautifulSoup(fetched_url.text, "html.parser")
    raw_data = store_data(beautifulsoup)
    dataframe = export_results(raw_data)
    pd.testing.assert_series_equal(df["Store"], dataframe["Store"], check_index=False, check_categorical = False)
    # beavis.assert_pd_column_equality(df, "col1", "col2")







if __name__ == "__main__":
    test_search_city()