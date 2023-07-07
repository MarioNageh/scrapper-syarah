import hashlib
from django.utils import timezone
from selenium.webdriver.common.by import By
from scrapper.modules.scrapping_dom import Dom


class Car:
    def __init__(self, name, status, price, image_url, currency):
        self.name = name
        self.__status = status
        self.price = price
        self.image_url = image_url
        self.currency = currency
        self.__hash = None
        self.scrapped_time = timezone.now()

    @property
    def hash(self):
        """
            Hash Car Values To , Help For Know Data Duplication
        """
        concatenated_string = str(self.name) + str(self.__status) + str(self.price) + str(self.image_url) + str(
            self.currency)
        hash_object = hashlib.sha256(concatenated_string.encode())
        return hash_object.hexdigest()

    @property
    def status(self):
        return "New" if self.__status == "جديدة" else "Used"

    @status.setter
    def status(self, value):
        self.status = value

    @staticmethod
    def from_browser_element(scrapper):
        """
            Convert Dom To Actually Car Object

        """

        img_ways = Dom.img_ways
        img_ulr = scrapper.many_find("Image", img_ways)

        name_ways = Dom.name_ways
        strong_name = scrapper.many_find("Name", name_ways)

        state_ways = Dom.state_ways
        strong_state = scrapper.many_find("State", state_ways)

        price_ways = Dom.price_ways
        strong_price_before_taxes = scrapper.many_find("Price", price_ways)

        name = strong_name.get_attribute("textContent").strip()
        state = strong_state.get_attribute("textContent").strip()

        url = img_ulr.get_attribute('src')
        price = strong_price_before_taxes.text
        currency = strong_price_before_taxes.find_element(By.TAG_NAME, 'span').get_attribute('innerHTML')
        price = price.replace(currency, "").strip()

        return Car(name, state, price, url, currency)

    def __str__(self):
        return f"Car: {self.name} -Status: {self.status} -Price: {self.price} -Image URL: {self.image_url}" \
               "-Currency: {self.currency} - Hash: {self.hash} "
