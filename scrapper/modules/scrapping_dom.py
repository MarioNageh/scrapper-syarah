from selenium.webdriver.common.by import By


class Dom:
    """
    This Class Have Static Values For All Dom Object That Help In Scrap
    """

    all_result_div = (By.XPATH, '/html/body/div[1]/div[1]/main/section/div[2]/div[3]')
    all_cars_Span = (By.XPATH, '/html/body/div[1]/div[1]/main/section/div[2]/div[2]/span')

    # Car Page Detail This Will Pass To Function That Try Handle Multiple Dom Structure
    img_ways = [
        (By.XPATH, '/html/body/div[1]/div[1]/main/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div/div[1]/div/img'),
    ]
    name_ways = [
        (By.CSS_SELECTOR, '.LeftColumn-module__carName'),
    ]
    state_ways = [
        (By.XPATH,
         '/html/body/div[1]/div[1]/main/div[1]/div[1]/div[1]/div[3]/div/div/div['
         '1]/div[2]/div[11]/strong'),
        (By.XPATH,
         '/html/body/div[1]/div[1]/main/div[1]/div[1]/div[1]/div[5]/div/div/div['
         '1]/div[2]/div[11]/strong')
    ]
    price_ways = [
        (By.CSS_SELECTOR, '.PaymentTabBox-module__price'),
        (By.CSS_SELECTOR, '.CashPayment-module__blkColor')
    ]

    # Loading
    list_of_loaders = [
        (By.CLASS_NAME,
         'BoxLoading-module__animatedBackground'),
        (By.CLASS_NAME, 'loader2022')
    ]