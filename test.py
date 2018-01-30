from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import urllib.request


def login(driver, username, password):
    driver.get("http://www.twitch.tv/user/login")
    elem_user = driver.find_element_by_id("username")
    elem_passwd = driver.find_element_by_name("password")
    elem_user.send_keys(username)
    elem_passwd.send_keys(password + Keys.RETURN)
    time.sleep(5)

def getClip(driver, link):
    driver.get(link)

    mature_menu = driver.find_element_by_css_selector(".pl-mature-overlay")
    mature_accept = driver.find_element_by_css_selector(".player-content-button")
    ActionChains(driver).move_to_element(mature_menu).click(mature_accept).perform()

    menu = driver.find_element_by_css_selector(".player-menu")
    hidden_submenu = driver.find_element_by_css_selector(".pl-clips-button")
    ActionChains(driver).move_to_element(menu).click(hidden_submenu).perform()

    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    form = soup.find("form", {"class" : "js-create-clip-form"})
    broadcast_ID = soup.find("input", {"class" : "js-create-clip-broadcast_id"})['value']
    offset_time = soup.find("input", {"class" : "js-create-clip-offset"})['value']

    clip_url = "https://clips-media-assets.twitch.tv/raw_media/" + broadcast_ID + "-offset-" + offset_time + ".mp4"
    print (clip_url)
    urllib.request.urlretrieve(clip_url, 'same.mp4')

username = "bungusbot2"
password = "monkabot"

driver = webdriver.Chrome()
login(driver, username, password)
getClip(driver, "https://twitch.tv/lilypichu")
