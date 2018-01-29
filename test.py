import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

my_username = "bungusbot"
my_password = "monkabot"

driver = webdriver.Chrome()
driver.get("http://www.twitch.tv/user/login")
elem_user = driver.find_element_by_id("username")
elem_passwd = driver.find_element_by_name("password")
elem_user.send_keys(my_username)
elem_passwd.send_keys(my_password + Keys.RETURN)

time.sleep(5)

driver.get("https://twitch.tv/lilypichu")

mature_menu = driver.find_element_by_css_selector(".pl-mature-overlay")
mature_accept = driver.find_element_by_css_selector(".player-content-button")
ActionChains(driver).move_to_element(mature_menu).click(mature_accept).perform()

menu = driver.find_element_by_css_selector(".player-menu")
hidden_submenu = driver.find_element_by_css_selector(".pl-clips-button")
ActionChains(driver).move_to_element(menu).click(hidden_submenu).perform()
