import time
from winsound import Beep

from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver, EventFiringWebElement

def beep(freq=200, duration=2):
    Beep(freq, duration)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class GamelogListener(AbstractEventListener):
    def after_change_value_of(self, element, driver):
        print("elem changed: ", element)

    def after_click(self, element, driver):
        print("clicked on: ", element)

    def after_navigate_to(self, url, driver):
        print("navigated to:", url)

    def after_execute_script(self, script, driver):
        print("exected script: ", script)
        
    def after_find(self, by, value, driver):
        print("found", value)


def wait_for_presence_of_element(name, by, waittime=10):
    wait = WebDriverWait(ef_driver, waittime)
    try:
        return wait.until(EC.presence_of_element_located((getattr(By, by), name)))
    except:
        print("da lief was schief")

google = "https://www.google.de/"
dominion_url = "https://dominion.games/"

browser = webdriver.Firefox()
browser.implicitly_wait(10)  #seconds
ef_driver = EventFiringWebDriver(browser, GamelogListener())
ef_driver.get(dominion_url)
# ef_driver.implicitly_wait(15)

try:
    username_input = wait_for_presence_of_element("username-input", "ID")
    username_input.clear()
    username_input.send_keys("schlafi")
except:
    print("Da kam nix! :(")

try:
    passwd_input = wait_for_presence_of_element("password", "NAME")
    passwd_input.clear()
    passwd_input.send_keys("ganxta89")
    print("login form filled")
    ef_driver.implicitly_wait(5)
    passwd_input.send_keys(Keys.ENTER)
except:
    print("login fail")

ng_click = "[@ng-click='$ctrl.automatch.botMatch(1)']"

# try:
#     ef_driver.implicitly_wait(10)
#     buttons = ef_driver.find_elements_by_xpath("//button")
#     if buttons:
#         for button in buttons:
#             print(button.text)
#             print(button.get_attribute("class"))
#             print(button.get_attribute("ng-click"))
# except:
#     print("keine buttons gefunden")

try:
    ef_driver.implicitly_wait(10)
    xpath = '//button[@ng-click="$ctrl.automatch.botMatch(1)"]'
    button = ef_driver.find_element_by_xpath(xpath)
    print("button gefunden")
    # button = wait_for_presence_of_element(xpath, "XPATH")
    if button:
        print(button.text)
        button.click()
except:
    print("button nicht gefunden")

try:
    ef_driver.implicitly_wait(10)
    cards = ef_driver.find_elements_by_class_name("card-name")
    if cards:
        for card in cards:
            print(card.text)
except:
    print("keine karten gefunden")

cards = {}
try:
    ef_driver.implicitly_wait(10)
    baseSupplyCardsContainer = ef_driver.find_element_by_class_name("base-hero-bar")
    if baseSupplyCardsContainer:
        baseSupplyCards = baseSupplyCardsContainer.find_elements_by_class_name("visible-supply")
        print(len(baseSupplyCards))
        for card in baseSupplyCards:
            card_name = card.find_element_by_class_name("full-card-name-container").text
            card_count = card.find_element_by_class_name("new-card-counter-text").text
            # print(card_name, card_count)
            cards.update({card_name: card_count})
    else:
        print("keine base karten gefunden")
except:
    print("error beim basekarten lesen")

try:
    kingdomSupplyContainer = ef_driver.find_element_by_class_name("supply")
    if kingdomSupplyContainer:
        kingdomSupplyCards = kingdomSupplyContainer.find_elements_by_class_name("visible-supply")
        print(len(kingdomSupplyCards))
        for card in kingdomSupplyCards:
            card_name = card.find_element_by_class_name("full-card-name-container").text
            card_count = card.find_element_by_class_name("new-card-counter-text").text
            # print(card_name, card_count)
            cards.update({card_name: card_count})
    else:
        print("keine kingdom karten gefunden")
except:
    print("error beim kingdom karten lesen")

hand = {}

try:
    handCardsContainer = ef_driver.find_element_by_class_name("hand")
    if handCardsContainer:
        handCards = handCardsContainer.find_elements_by_class_name("my-visible-hand")
        print(len(handCards))
        for card in handCards:
            card_name = card.find_element_by_class_name("full-card-name-container").text
            card_count = card.find_element_by_class_name("new-card-counter-text").text
            # print(card_name, card_count)
            hand.update({card_name: card_count})
    else:
        print("keine handkarten gefunden")
except:
    print("error beim handkarten lesen")


# gamelog = EventFiringWebElement(ef_driver.find_element_by_class_name("game-log"), ef_driver)
# if gamelog:
#     print("gamelog gefunden")

while True:
    ef_driver.implicitly_wait(2)

# try:
#     log_elems = browser.find_elements_by_class_name("actual-log")
#     if log_elems:
#         for i, elem in enumerate(log_elems):
#             print(i, elem.text)
# except:
#     print("fehler beim gamelog lesen")


# browser.close()

beep()