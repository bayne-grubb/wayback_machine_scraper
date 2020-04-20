import os
import json
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

page_base = "https://web.archive.org/web/"
star_slash_and_zeros = "0000000000*/"
years = ["2016", "2017", "2018", "2019", "2020"]
urls = ["www.bloomberg.com", "www.barrons.com", "www.wsj.com"]

driver_path = '/home/bayne/Documents/rich-face-detector/chromedriver'
target_path = '.'
df = pd.DataFrame()
for news_source in news_sources:
    break
    folder_name = news_source.split(".")[1]
    for year in years:
        target_url = page_base + year + star_slash_and_zeros + news_source
        #print(target_url)
        with webdriver.Chrome(executable_path=driver_path) as driver:
            driver.get(target_url)
            try:
                driver.maximize_window()
                element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        "//*[@id='react-wayback-search']/div[4]/div[2]/div[1]/div[2]"
                    )))
                time.sleep(5)
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                for month in range(1, 13):
                    month_xpath = "//*[@id='react-wayback-search']/div[4]/div[2]/div[{}]/div[2]".format(
                        month)
                    month_element = driver.find_element_by_xpath(month_xpath)
                    days = month_element.find_elements_by_tag_name("a")
                    url_list = []
                    for day in days:
                        try:
                            action = webdriver.ActionChains(driver)
                            action.move_to_element(day)
                            action.perform()
                        except:
                            pass
                        print("owo")
                        #time.sleep(1200)
                        element = WebDriverWait(driver, 60).until(
                            EC.presence_of_element_located((
                                By.XPATH,
                                "//*[@id='react-wayback-search']/div[4]/div[3]/div/div[2]/ul/div/div/li"
                            )))
                        pop_up = driver.find_element_by_xpath(
                            "//*[@id='react-wayback-search']/div[4]/div[3]/div/div[2]/ul/div"
                        )
                        snapshots = pop_up.find_elements_by_tag_name("a")
                        print("uwu")
                        url = random.sample(snapshots,
                                            1)[0].get_attribute("href")
                        print(url)
                        url_list.append(url)

                    target_folder = os.path.join(target_path, folder_name,
                                                 year, str(month))
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    with open(
                            os.path.join(target_folder,
                                         "{}.json".format(month)), "w") as f:
                        json.dump(url_list, f)
            finally:
                driver.quit()


driver = webdriver.Chrome(executable_path=driver_path)

def get_directories():
    return filter(os.path.isdir, sorted(os.listdir(os.getcwd())))


for website in get_directories():
    os.chdir(website)
    for year in get_directories():
        break
        os.chdir(year)
        for month in get_directories():
            month_path = os.path.join(month, "{}.json".format(month))
            print(year, month)
            df = pd.DataFrame(columns=["Date", "Text"])
            with open(month_path, "r") as month_file:
                for url in json.load(month_file):
                    text = ""
                    url_timestamp = url.split("/")[4]
                    timecode_year = url_timestamp[:4]
                    timecode_month = url_timestamp[4:6]
                    day = url_timestamp[6:8]
                    timecode = timecode_year + "-" + timecode_month + "-" + day
                    if int(timecode_month) != int(month):
                        continue
                    driver.get(url)
                    try:
                        WebDriverWait(driver,
                                  600).until(EC.presence_of_element_located((By.TAG_NAME,"p")))
                    except:
                        print("Skipping page because of timeout " +
                              timecode)
                        continue
                    try:
                        element = WebDriverWait(driver,
                                                1).until(EC.presence_of_element_located((By.XPATH,
                                                "//*[contains(text(), 'any URLs in the email')]"
                                                )))
                        if element:
                            print("Going to bed because I was told to")
                            time.sleep(420)
                            driver.get(url)
                            time.sleep(10)
                    except:
                        if random.randint(0,100) < 42:
                            print("Taking a snooze cuz I'm nice")
                            time.sleep(11)
                    try:
                        element = WebDriverWait(driver,
                                  1).until(EC.presence_of_element_located((By.XPATH,
                                                                             "//*[contains(text(),'Page Not Found')]")))
                        if element:
                            print("Skipping 404 error page for timecode: " +
                              timecode)
                            continue
                    except:
                        time.sleep(3)
                    try:
                        element = WebDriverWait(driver,
                                  1).until(EC.presence_of_element_located((By.XPATH,
                                                                             "//*[contains(text(),'HTTP 301')]")))
                        if element:
                            print("Skipping redirected page for timecode: " +
                              timecode)
                            time.sleep(10)
                            continue
                    except:
                        print("Checking for additional redirects: " + timecode)
                    try:
                        element = WebDriverWait(driver,
                                  1).until(EC.presence_of_element_located((By.XPATH,
                                                                             "//*[contains(text(),'HTTP 302')]")))
                        if element:
                            print("Skipping redirected page for timecode: " +
                              timecode)
                            time.sleep(10)
                            continue
                    except:
                        print("Harvesting text for timecode: " + timecode)
                    for paragraphs in driver.find_elements_by_tag_name('p'):
                        text = text + " " + paragraphs.text
                    df = df.append({"Date" : timecode, "Text" : text}, ignore_index=True)
                    if int(day) % 5 == 0:
                        time.sleep(11)
        os.chdir("..")
        time.sleep(300)
    os.chdir("..") 
    if not os.path.exists('csvs'):
        os.makedirs('csvs')
    df.to_csv('./csvs/' + website + "_" + year + "_" + month + "_" + "news_data.csv")



