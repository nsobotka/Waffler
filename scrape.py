from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import math
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

def convertToSquare(l):
    puzzle = [[''] * 5 for i in range(5)]
    counter = 0
    for i in range(0, 25):
        if (i != 6 and i != 8 and i != 16 and i != 18) :
            puzzle[math.floor(i / 5)][i % 5] = l[counter]
            counter = counter + 1
    return puzzle

def scrapeWeb():
    chromeOptions = Options()
    chromeOptions.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chromeOptions)
    driver.get('https://wafflegame.net/')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.prettify()
    split = soup.splitlines()
    l = []
    colors = []
    for i in range(0, len(split)):
        if "<div class=\"tile draggable tile" in split[i]:
            if "green" in split[i]:
                colors.append(('#6fb05c', '#FFFFFF'))
            elif "yellow" in split[i]:
                colors.append(('#e9ba3a', '#FFFFFF'))
            else:
                colors.append(('#edeff1', '#000000'))
            l.append(split[i + 1].strip())
    driver.quit()
    
    return convertToSquare(l), convertToSquare(colors)