# Imports
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def createDriver():
    """
    Creates a Chrome WebDriver and adds options to minimize chances of being detected as a bot.

    :return: a Chrome Webdriver instance
    """
    options = Options()

    # Suppress errors (INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3), default 0
    options.add_argument('--log-level=3')

    # Specifies if the ChromeDriver should remain after the completion of the script
    options.add_experimental_option("detach", False)

    # Add defensive options to prevent auto-detection of Selenium / ChromeDriver
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Disable loading of images to reduce data usage
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    # Create a new webdriver with provided options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0, print_first_line=False).install()),
                              options=options)

    return driver


def getCollections(driver):
    """
    Finds each collection and their associated URL from the Bear Library homepage

    :param driver: A ChromeDriver instance
    :return: a list of all collections and their associated URL
    """
    collections = []
    wrapper = driver.find_element(By.CLASS_NAME, "library-list")
    items = wrapper.find_elements(By.TAG_NAME, "li")
    for collection in items:
        collections.append({
            'collection_title': collection.find_element(By.CLASS_NAME, "library-title").text,
            'collection_url': collection.find_element(By.TAG_NAME, "a").get_attribute("href")
        })

    return collections


def getBearsFromCollection(driver, collection_url):
    """
    Gets a list of bears for a given collection and returns an dictionary containing the name and link of each bear

    :param driver: A ChromeDriver instance
    :param collection_url The URL of the Collection on the Charlie Bears Bear Library
    :return: a dictionary containing the name and URL of the bears in the collection
    """
    driver.get(collection_url)
    container = driver.find_element(By.CLASS_NAME, "bear-group-wrapper")
    bears = []
    for group in container.find_elements(By.CLASS_NAME, "bear-group"):
        for bear in group.find_elements(By.CLASS_NAME, "bear-item"):
            bears.append({
                "name": bear.find_element(By.TAG_NAME, "a").text,
                "url": bear.find_element(By.TAG_NAME, "a").get_attribute("href"),
            })

    return bears


def getBearDetails(driver, bear_url):
    """
    Scrapes data for a given bear and returns an object containing said data

    :param driver: A ChromeDriver instance
    :param bear_url The URL of the bear on the Charlie Bears Bear Library
    :return: a dictionary containing the scraped data of a singular bear
    """
    driver.get(bear_url)
    bear_content = driver.find_element(By.CLASS_NAME, "bear-content")
    image = driver.find_element(By.CLASS_NAME, "bear-image").value_of_css_property("background-image")

    return {
        'bear_name': bear_content.find_element(By.TAG_NAME, "h2").text.replace("Name ", ""),
        'bear_code': bear_content.find_elements(By.TAG_NAME, "p")[0].text.replace("Code\n", ""),
        'bear_collection': bear_content.find_elements(By.TAG_NAME, "p")[1].text.replace("Collection\n", ""),
        'bear_year': bear_content.find_elements(By.TAG_NAME, "p")[2].text.replace("Year\n", ""),
        'bear_height_paws': bear_content.find_elements(By.TAG_NAME, "p")[3].text.replace("Height in bear paws\n", ""),
        'image_url': image.lstrip('url("').rstrip('")'),
        'bear_library_url': driver.current_url
    }


def __init__():
    """
    init function
    """
    # Create a driver and change webdriver "navigator" value to undefined
    driver = createDriver()
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Navigate to the bear library page
    driver.get("https://www.charliebears.com/bear-library/")

    # Get all of the collections
    collections = getCollections(driver)

    allData = []

    # For each collection, get each bear's data and append to the allData object
    for collection in collections:
        bears = getBearsFromCollection(driver, collection['collection_url'])
        collection_details = []
        for bear in bears:
            collection_details.append(getBearDetails(driver, bear['url']))

        allData.append({
            'collection': collection['collection_title'],
            'collection_url': collection['collection_url'],
            'bears': collection_details
        })

    # Write out to output.json
    with open('output.json', 'w') as file:
        file.write(json.dumps(allData))


__init__()
