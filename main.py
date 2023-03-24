from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pandas as pd
import numpy as np
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


starttime = time.time()
PATH = "/Users/kay/PycharmProjects/selenium_health/chromedriver"
service = Service(PATH)
driver = WebDriver(service=service)
driver.implicitly_wait(1)

url = "https://www.healthgrades.com/usearch?what=Family%20Medicine&distances=National"
driver.get(url)

press = driver.find_elements(by=By.CLASS_NAME, value='pRyBq')

link_list = []

page_count = 0

while True:
    doctor_links = driver.find_elements(by=By.CLASS_NAME, value='card-name')
    # find doctors' personal webpage links
    for doctor_link in doctor_links:
        link = doctor_link.find_element(by=By.TAG_NAME, value='a')
        # store each link to a empty list
        link_list.append(link.get_attribute('href'))

    nextpage = driver.find_elements(By.XPATH, '//*[@id="search-results"]/div/div[2]/div[2]/div[1]/nav/ul/li/a')
    page_count = page_count+1
    # print(pagecount)
    if page_count == 1:
        break
    # click to next page
    driver.execute_script("arguments[0].click();", nextpage[-1])
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-name')))


all_details = []
for i in tqdm(link_list):
    driver = WebDriver(service=service)
    driver.get(i)
    d_name = driver.find_element(by=By.TAG_NAME, value='h1').text
    d_speciality = driver.find_element(By.CSS_SELECTOR, 'span[data-qa-target = "ProviderDisplaySpeciality"]').text
    total_score = driver.find_element(By.CSS_SELECTOR, 'div.overall-rating p').text
    total_survey_count = driver.find_element(By.CSS_SELECTOR, 'div.overall-rating div p').text
    five_star = driver.find_element(By.CSS_SELECTOR, 'table.breakdown-table tr td').text
    five_star_percentage = driver.find_element(By.CSS_SELECTOR, 'table.breakdown-table tr td.breakdown-table__bar span').text
    four_star = driver.find_element(By.CSS_SELECTOR, 'table.breakdown-table tbody tr:nth-child(2) td').text
    four_star_percentage = driver.find_element(By.CSS_SELECTOR, 'table.breakdown-table tbody tr:nth-child(2) td.breakdown-table__bar span').text
    three_star = driver.find_element(By.CSS_SELECTOR,
                                     'table.breakdown-table tbody tr:nth-child(3) td').text
    three_star_percentage = driver.find_element(By.CSS_SELECTOR,
                                               'table.breakdown-table tbody tr:nth-child(3) td.breakdown-table__bar span').text

    two_star = driver.find_element(By.CSS_SELECTOR,
                                               'table.breakdown-table tbody tr:nth-child(4) td').text
    two_star_percentage = driver.find_element(By.CSS_SELECTOR,
                                  'table.breakdown-table tbody tr:nth-child(4) td.breakdown-table__bar span').text
    one_star = driver.find_element(By.CSS_SELECTOR,
                                  'table.breakdown-table tbody tr:nth-child(5) td').text
    one_star_percentage = driver.find_element(By.CSS_SELECTOR,
                                  'table.breakdown-table tbody tr:nth-child(5) td.breakdown-table__bar span').text
    tempJ = {
        'd_name': d_name,
        'd_speciality': d_speciality,
        # 'd_age': d_age,
        # 'd_gender': d_gender,
        'total_score': total_score,
        'total_num_rate': total_survey_count,
        '5star': five_star,
        '5_percentage': five_star_percentage,
        '4star': four_star,
        '4_percentage': four_star_percentage,
        '3star': three_star,
        '3_percentage': three_star_percentage,
        '2star': two_star,
        '2_percentage':two_star_percentage,
        '1star': one_star,
        '1_percentage':one_star_percentage,
    }
    all_details.append(tempJ)
    driver.close()
df = pd.DataFrame(all_details)
df.to_csv('doctor.csv')
endtime = time.time()
print((endtime-starttime))