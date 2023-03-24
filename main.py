from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pandas as pd
import numpy as np
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# with open('doctor.csv', 'w') as f:
#     f.write()
PATH = "/Users/kay/PycharmProjects/selenium_health/chromedriver"
service = Service(PATH)
driver = WebDriver(service=service)
driver.implicitly_wait(10)

url = "https://www.healthgrades.com/usearch?what=Family%20Medicine&distances=National"
driver.get(url)

press = driver.find_elements(by=By.CLASS_NAME, value='pRyBq')

link_list = []

page_count = 0
condition = True
while condition:
    doctor_links = driver.find_elements(by=By.CLASS_NAME, value='card-name')
    # find doctors' personal webpage links
    for doctor_link in doctor_links:
        link = doctor_link.find_element(by=By.TAG_NAME, value='a')
        link_list.append(link.get_attribute('href'))
        # d_speciality = driver.find_element(By.CSS_SELECTOR, '.provider-info__specialty span').text
        #store each link to a empty list
    nextpage = driver.find_elements(By.XPATH, '//*[@id="search-results"]/div/div[2]/div[2]/div[1]/nav/ul/li/a')
    page_count = page_count+1
    # print(pagecount)
    if page_count == 1:
        condition = False
    # click to next page
    driver.execute_script("arguments[0].click();", nextpage[-1])


all_details = []
for i in tqdm(link_list):
    driver = WebDriver(service=service)
    driver.get(i)
    d_name = driver.find_element(by=By.TAG_NAME, value='h1').text
    # d_speciality = driver.find_elements(By.CSS_SELECTOR, '.summary-header-row-specialty span')


    tempJ = {
        'd_name': d_name,
        # 'd_speciality': d_speciality,
        # 'd_age': d_age,
        # 'd_gender': d_gender,
        # 'total_score': total_score,
        # 'total_num_rate': total_num_rate,
        # '5star': 5star,
        # '4star': 4star,
        # '3star': 3star,
        # '2star': 2star,
        # '1star': 1star,
    }
    all_details.append(tempJ)
    driver.close()
df = pd.DataFrame(all_details)
df.to_csv('doctor.csv')
