from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import random
import os

### 0: INPUTS

verbose = True        # print the output?
outdir = './output/'  # directory to save output in text files
if not os.path.isdir(outdir):  # check for existence of outdir, make if needed
    os.mkdir(outdir)

driver_path = '/usr/bin/chromedriver'   # webdriver, in this case must use chrome
url = 'https://www.faxvin.com/license-plate-lookup/illinois' # url to scrape


### 1: PLATES TO CHECK

# plates = ['CD45880', 'CD45881'] # test!
plates = []
for d1 in [3,5,9]:              # three possible first digits
    for d234 in range(1000):    # unsure of middle digits
        plate = f'DC{d1}{d234:03}8'
        if plate.count('3')==2: # check for two 3s
            if ~os.path.exists(os.path.join(outdir, plate+'.txt')):   # check if data already exists in a file
                plates.append(plate)


### 2: LOOP, DRIVER INSTANCE FOR EACH PLATE

for plate in plates:
    if verbose:
        print(plate)
        print()

    # create new webdriver instance
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    time.sleep(random.random()) # sleep some time, so website (hopefully) ignores bot

    # identify the search bar
    search_bar = driver.find_element('name', 'plate')

    for letter in plate:  # send letters one at a time (bot tricking)
        time.sleep(random.random()/10)
        search_bar.send_keys(letter)
    search_bar.send_keys('\n')

    # wait for results to load, then write output
    the_class_name = "tableinfo"
    try: 
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, the_class_name))
                )
    except Exception as e:
        print(e)
        driver.quit()
    
    search_results = driver.find_element(By.CLASS_NAME, the_class_name)

    if verbose:
        print(search_results.text)
        print()

    with open(outdir+plate+'.txt', 'w') as f:
        f.write(search_results.text)

    driver.quit()


