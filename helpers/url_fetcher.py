from selenium import webdriver
from bs4 import BeautifulSoup
import time
from bs4.element import Tag
from webdriver_manager.chrome import ChromeDriverManager
gChromeOptions = webdriver.ChromeOptions()
gChromeOptions.add_argument('--disable-gpu')
gChromeOptions.add_argument('--no-sandbox')
#driver = webdriver.Chrome('D:/Downloads/Projects/chromedriver')
driver = webdriver.Chrome(
    chrome_options=gChromeOptions, executable_path=ChromeDriverManager().install()
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
    data[0] =list(dict.fromkeys(data[0]))
    data[1] = list(dict.fromkeys(data[1]))
    return data
