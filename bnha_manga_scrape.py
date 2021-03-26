import os
import time

import requests
import shutil
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException


def get_soup(link):
    driver = webdriver.Edge("C:/location_of_the_driver/msedgedriver.exe")
    driver.set_page_load_timeout(5)
    try:
        driver.get(link)
        time.sleep(10)  # wait for the browser to be checked
    except TimeoutException:
        pass
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()
    return soup


def get_chapter(latest=True):
    soup = get_soup("http://kissmanga.com/Manga/Boku-no-Hero-Academia")
    x = soup.find("table", class_="listing")
    new = x.find('a')
    if latest:
        # download only one chapter (the latest one) 
        return 'http://kissmanga.com' + new.get('href'), new.text.strip()
    for y in x.findAll("a"):
        # download chapters while the user inputs yes
        link = 'http://kissmanga.com' + y.get('href')
        user_in = input("Download " + y.text.strip() + "? \n")
        if user_in in ('yes', 'Y', 'y', 'yeah', 'YES', 'Yes', 'yo'):
            get_page_links(link, y.text.strip())
        else:
            break
    return None

    
def get_page_links(link, title):
    # print(title)
    soup = get_soup(link)
    x = soup.find('div', id='divImage')
    image_links = []
    for each in x.findAll('p'):
        z = each.find('img').get('src')
        image_links.append(z)

    ch_number = title[26:].replace(':', ' -')
    # title is of the form "Read Boku no Hero Academia {ch_number} online"
    # len('Read Boku no Hero Academia ') = 27

    download_pages(image_links, ch_number)
    return None


def download_pages(links, chapter):
    i = 1
    os.mkdir(str(chapter))  # make a new folder for the chapter
    for link in links:
        filename = '{0}/bnha{1}_{2}.png'.format(chapter, chapter[:3], i)
        response = requests.get(link, stream=True)
        print('Downloading page: {} (of {})...'.format(i, len(links)))
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        i += 1
    print('DOWNLOAD COMPLETE!')
    return None


if __name__ == "__main__":   
    get_chapter(latest=True)
