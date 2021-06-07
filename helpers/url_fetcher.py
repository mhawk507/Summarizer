import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from bs4.element import Tag

gChromeOptions = webdriver.ChromeOptions()
gChromeOptions.binary_location = os.getenv("GOOGLE_CHROME_BIN")
gChromeOptions.add_argument('--headless')
gChromeOptions.add_argument('--no-sandbox')
gChromeOptions.add_argument('--disable-gpu')
#driver = webdriver.Chrome('D:/Downloads/Projects/chromedriver')
driver = webdriver.Chrome(
    executable_path=os.getenv("CHROMEDRIVER_PATH"),chrome_options=gChromeOptions
)

def fetch_url(query):
    google_url = "https://www.google.com/search?q=" + query + "&num=" + str(15)
    driver.get(google_url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    result_div = soup.find_all('div', attrs={'class': 'g'})
    links = []
    titles = []
    descriptions = []
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href=True)
            title = None
            title = r.find('h3')

            if isinstance(title,Tag):
                title = title.get_text()

            description = None
            description = r.find('span', attrs={'class': 'st'})

            if isinstance(description, Tag):
                description = description.get_text()

            # Check to make sure everything is present before appending
            if link != '' and title != '' and description != '':
                links.append(link['href'])
                titles.append(title)
                descriptions.append(description)
        # Next loop if one element is not present
        except Exception as e:
            print(e)
            continue
    return [titles, links]


def url_fetcher(query):
    data = fetch_url(query)
    remove_data_0 = []
    remove_data_1 = []
    for i in data[1]:
        if (not i.startswith('http')) or i.endswith('.pdf') or i.startswith('/'):
            remove_data_1.append(i)
            index = data[1].index(i)
            print(index)
            remove_data_0.append(data[0][index])

    if len(remove_data_0) > 0:
        for i in range(0, len(remove_data_0)):
            data[0].remove(remove_data_0[i])
            data[1].remove(remove_data_1[i])

    res = dict(zip(data[0], data[1]))
    data[0]=list(res.keys())
    data[1]=list(res.values())

    return data
