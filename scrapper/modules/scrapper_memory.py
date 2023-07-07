from dataclasses import dataclass, field


@dataclass
class Memory:
    """
    This Class Helping In Save Last State
    So If You Close The Scrapper, any error happen , it will continue form where
    it closed

    this object will store in Database
    """
    total_scrapped_item: int = 0
    last_scrapped_item: object = None
    last_scrolled_page_number: int = 0
    scrapped_items: list = field(default_factory=list)
    last_scrapped_item_number: int = 0

    total_cars = 0

    """
        this is queue of links to get data after collect some links
    """
    list_of_links_to_be_scrapped: list = field(default_factory=list)
    last_link_found_number = 0

    session_scrapped_items_count = 0

    def __post_init__(self):
        if self.scrapped_items is None:
            self.scrapped_items = []

        if self.list_of_links_to_be_scrapped is None:
            self.list_of_links_to_be_scrapped = []
