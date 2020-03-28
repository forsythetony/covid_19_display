import requests 
from bs4 import BeautifulSoup
import logging as log
# from requests.exceptions import RequestException

HENNEPIN_URL = "https://www.health.state.mn.us/diseases/coronavirus/situation.html"
MINNESOTA_URL = "https://www.health.state.mn.us/diseases/coronavirus/situation.html"
US_URL = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html"

class CovidRetriever():

    def __init__(self):
        pass

    def get_count_for_hennepin(self, response=None):
        try:
            if response is None: 
                response = requests.get(url = HENNEPIN_URL)
            return self.__extract_hennepin_co_count(response)
        except RequestException as rx:
            log.error("Failed to retrieve content from URL -> %s with exception -> %s", HENNEPIN_URL, str(rx))
            return -1

    def get_count_for_minnesota(self, response=None):
        try:
            if response is None: 
                response = requests.get(url = MINNESOTA_URL)
            return self.__extract_minnesota_state_count(response)
        except RequestException as rx:
            log.error("Failed to retrieve content from URL -> %s with exception -> %s", MINNESOTA_URL, str(rx))
            return -1
    
    def get_count_for_nation(self, response=None):
        try:
            if response is None: 
                response = requests.get(url = US_URL)
            return self.__extract_nation_count(response)
        except RequestException as rx:
            log.error("Failed to retrieve content from URL -> %s with exception -> %s", US_URL, str(rx))
            return -1

    def __extract_nation_count(self, raw_webpage):
        soup = BeautifulSoup(raw_webpage.content, 'html.parser')

        raw_text = soup.find('div', class_='2019coronavirus-summary').find("li").get_text().replace("Total cases: ", "").replace(",", "")

        return int(raw_text)

    def __extract_minnesota_state_count(self, raw_webpage):
        soup = BeautifulSoup(raw_webpage.content, 'html.parser')

        full_list_text = soup.find(id='body').find('ul').find('li').get_text()

        number_text = full_list_text.replace("Total positive: ", "")[0:11].splitlines()[0].strip()

        return int(number_text.replace(",",""))

    def __extract_hennepin_co_count(self, raw_webpage):
        soup = BeautifulSoup(raw_webpage.content, 'html.parser')

        tableRows = soup.find_all('tbody')[0].find_all("tr")

        raw_number = self.__get_count_for_county('Hennepin', tableRows)

        return int(raw_number.replace(",", ""))

    def __get_count_for_county(self, county_name, table_rows):
        count = 0

        for row in table_rows:
            cells = row.find_all("td")

            if len(cells) != 0:
                curr_county_name = cells[0].get_text()

                if curr_county_name.lower() == county_name.lower():
                    total_count = cells[1].get_text()
                    count = total_count


        return count
