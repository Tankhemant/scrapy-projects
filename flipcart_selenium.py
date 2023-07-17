from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver
import time
import pandas as pd

options = webdriver.ChromeOptions()
# options.add_argument('--blink-settings=imagesEnabled=false')
uc.TARGET_VERSION = 85
driver = uc.Chrome(options=options)
options.add_experimental_option("detach", True)
driver.get('https://www.flipkart.com/')
time.sleep(5)
driver.save_screenshot('datadome_undetected_webdriver.png')
driver.find_element(By.XPATH, "//input[@class='_3704LK']").send_keys(
    "MI Phones")
time.sleep(5)
driver.find_element(By.XPATH, "//form/div/button[@class='L0Z3Pu']").click()
time.sleep(5)

number = 1
nextisnot = True
while nextisnot:
    time.sleep(5)
    name = driver.find_elements(By.XPATH, "//div[@class='_4rR01T']")
    rating = driver.find_elements(
        By.XPATH, "//span[@class='_2_R_DZ']//span[contains(text(),'Ratings')]")
    price = driver.find_elements(By.XPATH, "//div[@class='_30jeq3 _1_WHN1']")
    imgpath = driver.find_elements(By.XPATH, "//div[@class='_2QcLo-']//img")

    RamRoms1 = []
    Displays1 = []
    Cameras1 = []
    Batterys1 = []
    for names in name:
        time.sleep(10)
        names.click()
        time.sleep(10)
        driver.switch_to.window(driver.window_handles[1])

        RamRoms = driver.find_element(
            By.XPATH, "//ul/li[@class='_21Ahn-'][1]").text
        Displays = driver.find_element(
            By.XPATH, "//ul/li[@class='_21Ahn-'][2]").text
        Cameras = driver.find_element(
            By.XPATH, "//ul/li[@class='_21Ahn-'][3]").text
        Batterys = driver.find_element(
            By.XPATH, "//ul/li[@class='_21Ahn-'][4]").text
        RamRoms1.append(RamRoms)
        Displays1.append(Displays)
        Cameras1.append(Cameras)
        Batterys1.append(Batterys)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    time.sleep(10)
    rates = [rate.text for rate in rating]
    names = [names.text for names in name]
    prices = [prices.text for prices in price]
    imgpaths = [path.get_attribute("src") for path in imgpath]

