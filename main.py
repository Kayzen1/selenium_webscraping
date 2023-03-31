from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def iselement(browser, cssselector):
    try:
        browser.find_element(By.CSS_SELECTOR, cssselector)
        return True
    except NoSuchElementException:
        return False

starttime = time.time()
PATH = "/Users/kay/PycharmProjects/selenium_health/selenium_webscraping/chromedriver"
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

all_details = []
rows = []
for i in tqdm(link_list):
    forloopstarttime = time.time()
    driver = WebDriver(service=service)
    driver.get(i)
    d_name = driver.find_element(by=By.TAG_NAME, value='h1').text
    d_speciality = driver.find_element(By.CSS_SELECTOR, 'span[data-qa-target = "ProviderDisplaySpeciality"]').text
    if (iselement(driver, 'div.ratings-wrapper')):
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

    driver.execute_script("window.scrollBy(0, 1000);")

    try:
        cookie_button = driver.find_element(By.CSS_SELECTOR, 'div#onetrust-close-btn-container button')
        cookie_button.click()
    except:
        pass

    positive_tags = []
    negative_tags = []
    if (iselement(driver, 'div.review-tagging-summary')):
        try:
            # click on "more" buttons
            more_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.link--secondary')))
            driver.execute_script("arguments[0].click();", more_button)
        except:
            pass

        try:
            po_tags = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul[class = "review-tagging-summary__list__experience review-tagging-summary__list__experience--good"] li span')))
            for tag in po_tags:
                positive_tags.append(tag.text)
        except:
            pass

        try:
            ne_tags = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul[class = "review-tagging-summary__list__experience review-tagging-summary__list__experience--bad"] li span')))
            for tag in ne_tags:
                negative_tags.append(tag.text)
        except:
            pass

        num_reviews_before = len(driver.find_elements(By.CSS_SELECTOR, 'div.c-single-comment__comment'))
        while True:
            try:
                # click on "more reviews"button
                more_reviews_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.c-comment-list__show-more')))

                driver.execute_script("arguments[0].click();", more_reviews_button)
                time.sleep(2)
                num_reviews_after = len(driver.find_elements(By.CSS_SELECTOR, 'div.c-single-comment__comment'))
                print(num_reviews_after, num_reviews_before)

                if num_reviews_after == num_reviews_before:
                    print("No new reviews loaded. End of reviews.")
                    break
                num_reviews_before = num_reviews_after
                more_comment_detail = None

                # check if "more details" button is present
                try:
                    more_comment_detail = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, 'div.c-single-comment__more-details button.link--secondary')))
                    driver.execute_script("arguments[0].click();", more_comment_detail)
                except:
                    pass

            except:
                print("No 'more' button found on the page.")
                break


        try:
            comments = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-qa-target="user-comment"]')))
            for comment in comments:
                comment_text = comment.text
                rows.append([d_name, d_speciality,total_score,total_survey_count,five_star, five_star_percentage, four_star, four_star_percentage,
                             three_star, three_star_percentage, two_star,two_star_percentage, one_star, one_star_percentage, positive_tags, negative_tags,
                             comment_text])
        except:
            pass

    # tempJ = {
    #     'd_name': d_name,
    #     'd_speciality': d_speciality,
    #     'total_score': total_score,
    #     'total_num_rate': total_survey_count,
    #     '5star': five_star,
    #     '5_percentage': five_star_percentage,
    #     '4star': four_star,
    #     '4_percentage': four_star_percentage,
    #     '3star': three_star,
    #     '3_percentage': three_star_percentage,
    #     '2star': two_star,
    #     '2_percentage': two_star_percentage,
    #     '1star': one_star,
    #     '1_percentage': one_star_percentage,
    #     'positive_tags': positive_tags,
    #     'negative_tags': negative_tags,
    # }
    # all_details.append(tempJ)
    forloopendtime = time.time()
    print(forloopendtime-forloopstarttime)
    driver.close()

# df = pd.DataFrame(all_details)
# df.to_csv('doctor.csv')


with open('doctor.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in rows:
        writer.writerow(row)

endtime = time.time()
print(endtime-starttime)