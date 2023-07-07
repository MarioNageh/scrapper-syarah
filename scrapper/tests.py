from django.test import TestCase
from django.urls import reverse
from selenium.webdriver.common.by import By

from scrapper.models import Car, CarModel
from scrapper.modules.scrapper import Scrapper
from scrapper.modules.scrapping_dom import Dom


class ScrapperTest(TestCase):
    def setUp(self):
        print("Setup New Test")
        self.scrapper = Scrapper()
        self.page_items_when_scroll = 12
        self.scrapper.start_session()
        url = "https://syarah.com/filters?is_online=1"
        self.scrapper.navigate(url)
        self.scrapper.update_total_car_numbers()

    def test_scrolling(self):

        self.scrapper.scroll()
        self.scrapper.scroll()
        self.scrapper.scroll()

        all_result_div = self.scrapper.try_until_find_element(*Dom.all_result_div)
        total_page_a_tag_founded = len(all_result_div.find_elements(By.TAG_NAME, "a"))

        self.assertEqual(self.scrapper.memory.last_scrolled_page_number, 3)
        self.assertEqual(total_page_a_tag_founded,
                         (self.scrapper.memory.last_scrolled_page_number + 1) * self.page_items_when_scroll)

    def test_getting_elements_until_function(self):
        self.scrapper.collect_main_page_link_until(50)
        self.assertEqual(self.scrapper.memory.last_link_found_number,50)


    def tearDown(self):
        self.scrapper.close()
