import re
from time import sleep
from os import environ
import requests as rq
from requests.exceptions import HTTPError, Timeout
import bs4
from bs4 import Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

SNAPSHOT_ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_URL = environ["FORM_LINK"]


class ListingInfo:
    def __init__(self) -> None:
        self.response_successful = None
        self.response = self.get_response()
        if self.response_successful:
            self.soup = bs4.BeautifulSoup(self.response.text, "html.parser")
            self.all_listings = self.get_listing_info()
        else:
            self.soup = None
            self.all_listings = None

    def get_response(self):
        """
        Queries the specifed website and checks for
        errors, if no error occurs the Object will
        set all of the class variables.
        """
        try:
            res = rq.get(SNAPSHOT_ZILLOW_URL, timeout=30)
            res.raise_for_status()
        except HTTPError as e:
            print(f"An error occured trying to connect to the website:\n{e}")
            self.response_successful = False
            return res
        except Timeout as e:
            print(f"The website took to long to respond:\n{e}")
            self.response_successful = False
            return res
        self.response_successful = True
        return res

    def get_listing_info(self):
        """
        Gets and formats the information
        scrapped from the copy of the Zillow
        website and sets the self.all_listings
        variable.
        """
        li_list = self.soup.find("ul", class_=re.compile("photo-cards")).find_all_next(
            "li", class_=re.compile("StyledListCardWrapper")
        )
        all_listings = [self._return_listing_info(elem) for elem in li_list]
        return all_listings

    def _format_price(self, raw_text: str):
        c_text = raw_text.split("+")[0].strip("/mo")
        if "," not in c_text:
            str_list = list(c_text)
            str_list.insert(2, ",")
            c_text = "".join(str_list)
        return c_text

    def _format_address(self, raw_text: str):
        c_text = raw_text.strip()
        if "|" in c_text:
            c_text = c_text.split("|")[1]
        n_list = c_text.split(",")
        n_list.reverse()
        state_zip = n_list[0].strip()
        city = n_list[1].strip()
        address = n_list[2].strip()

        return f"{address}, {city}, {state_zip}"

    def _return_listing_info(self, element: Tag):
        a_elem = element.find_next("a", class_=re.compile("-anchor"))
        url = a_elem["href"]
        address = self._format_address(a_elem.find_next("address").text)
        price = self._format_price(
            element.find_next("span", class_=re.compile("StyledPriceLine")).text
        )
        return (address, price, url)


listing_info = ListingInfo()

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options)

for listing in listing_info.all_listings:
    browser.get(FORM_URL)
    try:
        WebDriverWait(browser, 60).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".Qr7Oae input"))
        )
    except TimeoutException:
        print("Page took to long to load.")
    else:
        input_elems = browser.find_elements(By.CSS_SELECTOR, ".Qr7Oae input")
        submit_button = browser.find_element(By.XPATH, "//span[contains(text(), 'Submit')]")
        sleep(.2)
        for elem in input_elems:
            elem_i = input_elems.index(elem)
            elem.send_keys(listing[elem_i])
        sleep(.2)
        submit_button.click()

browser.quit()
