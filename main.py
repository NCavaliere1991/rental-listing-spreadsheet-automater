from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSfeI46w2Dwz30w0vv4WVfLc4LbUF8k0yazb_xnlRJlMqAZrlw/viewform?usp=sf_link"
ZILLOW_LINK = "https://www.zillow.com/homes/for_rent/1-1_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%2C%22max%22%3A1%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
CHROME_DRIVER_PATH = "/Users/nickcavaliere/Development/chromedriver"
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

response = requests.get(ZILLOW_LINK, headers=headers)
zillow_listings = response.text

soup = BeautifulSoup(zillow_listings, "html.parser")
listing_links = soup.select(".list-card-info a")

link_list = []
for listing in listing_links:
    link = listing.get("href")
    if "http" not in link:
        link_list.append(f"https://www.zillow.com{link}")
    else:
        link_list.append(link)

address_list = []
listing_addresses = soup.find_all(name="address", class_="list-card-addr")
for address in listing_addresses:
    address_list.append(address.text.split("|")[-1].strip())

price_list = []
listing_prices = soup.find_all(name="div", class_="list-card-price")
for price in listing_prices:
    if "$" in price.text:
        if "+" in price.text:
            listing_prices = soup.select(".list-card-details li")
            price_list.append(price.getText().split("+")[0])
        elif "/" in price.text:
            price_list.append(price.getText().split("/")[0])


for response in range(len(link_list)):
    driver.get(GOOGLE_FORM_LINK)

    time.sleep(2)
    address = driver.find_element_by_xpath("//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    price = driver.find_element_by_xpath("//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    link = driver.find_element_by_xpath("//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
    submit = driver.find_element_by_xpath("//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div/div/span/span")

    address.send_keys(address_list[response])
    price.send_keys(price_list[response])
    link.send_keys(link_list[response])
    submit.click()