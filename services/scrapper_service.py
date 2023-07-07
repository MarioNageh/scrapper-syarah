import threading
import time


from scrapper.models import Car, ScrapperMemory
from scrapper.modules.scrapper import Scrapper
from scrapper.utils import printer


class ScrapperService:
    def __init__(self, waiting_seconds):
        self.start_time = None
        self.scrapper = Scrapper()
        self.waiting_seconds = waiting_seconds
        self.thread = threading.Thread(target=self.__start_scrapping)

    def start(self):
        print(f"Scrapping Service Will Started After {self.waiting_seconds} Second")
        self.thread.start()

    def __start_scrapping(self):
        """
            This Start Scrapping In Other Thread

            Brings Memory From Database To Know
            from Where Starts


            this Example To Scrap 100 Car Item
            - To Scrap Full Items Modify This Function With
            self.scrapper.collect_main_page_from_to(self.scrapper.memory.last_scrapped_item_number,
                                                float('inf'))

            - To Scrap Item From To Call It Will  [ this Call Will scrap 100 New Items ]
            self.scrapper.collect_main_page_from_to(self.scrapper.memory.last_scrapped_item_number,
                                                self.scrapper.memory.last_scrapped_item_number + 100)
        """
        time.sleep(self.waiting_seconds)
        print(printer.green_fg(f"Scrapping Service Started"))

        # Getting Memory For Last Scrapped Data
        # if ScrapperMemory Empty Create It
        row_count = ScrapperMemory.objects.count()
        memory = None
        if row_count <= 0:
            memory = ScrapperMemory(total_scrapped_itme=0, last_scrolled_page=0, last_scrapped_item_number=0)
            memory.save()
        else:
            # Only One Row For Summary
            memory = ScrapperMemory.objects.get(id=1)

        self.scrapper.start_session()
        self.scrapper.memory.total_scrapped_item = memory.total_scrapped_itme
        self.scrapper.memory.last_scrapped_item_number = memory.last_scrapped_item_number

        url = "https://syarah.com/filters?is_online=1"
        self.scrapper.navigate(url)
        self.scrapper.update_total_car_numbers()

        self.scrapper.collect_main_page_from_to(self.scrapper.memory.last_scrapped_item_number,
                                                50)
        self.scrapper.scrap_save_items_in_memory()
        print(printer.green_fg(f"Scrapper Finished Scrapping"))