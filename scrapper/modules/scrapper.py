import re
import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrapper.models import Car, ScrapperMemory
from scrapper.modules.car import Car as CarModel
from scrapper.modules.exceptions import ElementNotFoundInDom
from scrapper.modules.scrapper_memory import Memory
from scrapper.modules.scrapping_dom import Dom
from scrapper.utils import printer
from scrapper.utils.utils import get_url_without_encoding


class Scrapper:
    _instance = None

    def __new__(cls):
        """
        Make Scrapper Singleton
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        inti object
        """
        self.driver: WebDriver = None
        self.scrapper = None
        self.navigation_stack = None
        self.ready_status = False
        self.memory: Memory = None
        self.show_navigation_debug = False

    def start_session(self, memory=None):
        """
            Start Driver Session
        """
        self.driver = webdriver.Chrome(options=self.set_chrome_options())
        self.scrapper = WebDriverWait(self.driver, 10)
        self.navigation_stack = []
        if not self.memory:
            self.memory = Memory()

    def close(self):
        """
            Close Old Session
        """
        self.driver.quit()
        del self.memory
        del self.scrapper
        del self.navigation_stack
        del self.driver

    def find_element(self, by, value):
        """
        Find Element In Current DOM
        :param by: (str): way to find
        :param value: (str): value to search
        :return: the element found in DOM Object
        """
        return self.driver.find_element(by, value)

    def try_until_find_element(self, by, value, number_of_tries=100):
        """
            This Function Try To Get Element
            If Not Found It try To Found It And Sleep 1 Seconds
            Tries till number of tries reach number_of_tries

            raise : ElementNotFoundInDom possible The Website Blocked You
        """
        tries = number_of_tries
        item = None
        while tries > 0:
            try:
                item = self.driver.find_element(by, value)
                break
            except:
                tries -= 1
                print(f"Trying Number {number_of_tries - tries}")
                time.sleep(1)
                continue
        if not item:
            raise ElementNotFoundInDom(f"Tries {number_of_tries} by Element Not Found,"
                                       f"Check If You Blocked")

        return item

    def find_element_wait(self, by, value):
        """
        Find Element by Waiting Seconds
        :param by: (str): way to find
        :param value: (str): value to search
        :return: the element found in DOM Object
        :raise : Timeout
        """
        return self.scrapper.until(
            EC.presence_of_element_located((by, value)))

    def scroll(self):
        """
            Scroll page , or Paginate The Page To Get More Data
        """
        self.memory.last_scrolled_page_number += 1
        print(printer.yellow_fg(f"Scrolling To {self.memory.last_scrolled_page_number}"))

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.wait_for_page_fully_loaded()

    def scroll_if_needed(self, number_of_a_tag_in_page, item_to_added):
        """
            this Will Scroll when item_to_added become
            bigger that items in Page
        """
        if number_of_a_tag_in_page < item_to_added:
            self.scroll()

    @staticmethod
    def default_waiting(seconds=2):
        print(f"--------------- Waiting [{seconds}] -----------")
        time.sleep(seconds)

    def wait_for_page_fully_loaded(self):
        """"
            This Function Wait till Page Fully Loaded
            and all loader dis-sapper

            this function is General So It Exit The Loop
            when loaders not found , because some pages using different
            loader in DOM
        """
        start_time = time.time()
        list_of_tries = Dom.list_of_loaders
        while True:
            founded = False
            for way in list_of_tries:
                try:
                    self.driver.find_element(way[0], way[1])
                    founded = True
                except:
                    pass
            time.sleep(2)  # will Stop For 2 Second To Render DOM If Even Success
            if not founded:
                break
        end_time = time.time()
        print(f"Page Loaded Completed in [{round(end_time - start_time, 2)}] s")

    def navigate(self, link):
        """
            this function make driver navigate To Link
            and Wait till Page Loaded
            push the link in stack to observe navigation in future
        """
        print(printer.yellow_fg(f"Navigating To -> '{get_url_without_encoding(link)}'"))
        self.driver.get(link)
        self.navigation_stack.append(get_url_without_encoding(link))
        self.wait_for_page_fully_loaded()

    def back(self, mode=False):
        """
        To Go to Last Page
        :param mode: if mode is True we Will Not Make A Call To Server
        to reduce Traffic
        :return: None
        """
        last_link = self.navigation_stack.pop()
        if self.show_navigation_debug:
            print(f"Navigate From {last_link} -----> {self.navigation_stack[-1]}")
        if not mode:
            self.driver.back()

    def many_find(self, attr_name, list_of_way):
        """
            this function try of find element
            by Search in DOM using Different Ways

            :return: Item In Dom
            :raise: ElementNotFoundInDom If No Way Success To Get Data
        """
        item = None
        if not list_of_way or len(list_of_way) <= 0:
            raise ValueError(f"list_of_way must be defined")

        for way in list_of_way:
            try:
                item = self.find_element(way[0], way[1])
            except:
                pass

        if not item:
            return ElementNotFoundInDom(f"Not Found {attr_name} in Doc")
        return item

    @staticmethod
    def set_chrome_options() -> Options:
        """
            Prepare The Chrome Driver
            No Gui , No Image Rendered , Escape Some Errors
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {"profile.default_content_settings": {"images": 2}}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        return chrome_options

    def scrap_save_items_in_memory(self):
        """
            this function Open Detail Page
            and Save Every Car in memory , and DataBase
        """

        if not self.memory.scrapped_items:
            self.memory.scrapped_items = []

        for link in self.memory.list_of_links_to_be_scrapped:
            self.navigate(link)
            new_car = CarModel.from_browser_element(self)

            self.memory.last_scrapped_item_number += 1
            self.memory.last_scrapped_item = new_car
            self.memory.total_scrapped_item += 1
            self.memory.scrapped_items.append(new_car)

            c = Car.insert(new_car)
            self.memory.last_scrapped_item = c
            ScrapperMemory.update_memory(self.memory)
            print(printer.green_fg(f"{c.name} - Scrapped Successfully"))

            self.back(True)

    def collect_main_page_from_to(self, from_item_number, to_item_number):
        """
            this function will get items between the range [from_item_number , to_item_number]
            this function will rearrange memory items so if
            you call it after sequential search it will
            play around with its values

        :param from_item_number: the car number in website
        :param to_item_number:  the car number in website
        :return: void
        """
        if to_item_number > self.memory.total_cars:
            to_item_number = self.memory.total_cars

        if from_item_number > to_item_number:
            raise ValueError("from must be small than to")

        self.collect_main_page_link_until(from_item_number)
        self.collect_main_page_link_until(to_item_number)

        self.memory.list_of_links_to_be_scrapped = self.memory.list_of_links_to_be_scrapped[
                                                   from_item_number:to_item_number]

    def collect_main_page_link_until(self, number_of_items):
        """
        this function prepare links for scrapping items
        is start from current location in memory till number_of_items
        make a scrolling to get this number
        :param number_of_items: number of items to be scrapped
        :return:
        """

        total_collected_items = 0
        list_of_elements = []

        # if number of item need to get bigger than website content
        # set the items number to be rest
        if self.memory.last_link_found_number + number_of_items > self.memory.total_cars:
            number_of_items = self.memory.total_cars - self.memory.last_link_found_number

        # Count Total <a> Tag In Page To Know We Need To Scroll Or Nor
        all_result_div = self.try_until_find_element(*Dom.all_result_div)
        total_page_a_tag_founded = len(all_result_div.find_elements(By.TAG_NAME, "a"))
        # Scrolling Handling
        while self.memory.last_link_found_number < number_of_items:
            self.scroll_if_needed(total_page_a_tag_founded, number_of_items)

            all_result_div = self.try_until_find_element(*Dom.all_result_div)
            total_page_a_tag_founded = len(all_result_div.find_elements(By.TAG_NAME, "a"))
            child_elements = all_result_div.find_elements(By.TAG_NAME, "a")[
                             self.memory.last_link_found_number:]

            remain_items_count = number_of_items - total_collected_items
            length_of_list_to_added = min(remain_items_count, len(child_elements))

            list_of_elements.extend(child_elements[0:length_of_list_to_added])
            self.memory.last_link_found_number += length_of_list_to_added
            total_collected_items += length_of_list_to_added

        # Getting Cars Links
        for el in list_of_elements:
            link = el.get_attribute("href")
            self.memory.list_of_links_to_be_scrapped.append(link)

    def update_total_car_numbers(self):
        """
        this function fetch car numbers in main page and update it to
        scrapper memory to limit scrolling , help calculation
        """
        item = self.find_element(*Dom.all_cars_Span)
        text = item.text
        match = re.search(r"\d+", text)
        if match:
            number = match.group()
            self.memory.total_cars = int(number)
        else:
            raise ElementNotFoundInDom("Not Found Number Of Elements In DOM")
