from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class ScraperException(Exception):
    pass

class WebsiteScraperException(ScraperException):
    pass

# Function to extract and display product details
def croma(name):
    try:
        # Initialize the driver
        chrome_options = ChromeOptions()
        chrome_options.headless = False
        webdriver_path = r"C:\\Users\\Amaan Shaikh\\OneDrive - RizviCollegeOfEngineering\\Desktop\\Price Comparison\\Backend\\chromedriver-win64\\chromedriver.exe"
        service = ChromeService(executable_path=webdriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # URL of the Croma search results page with the search query
        search_query = name

        url = f"https://www.croma.com/searchB?q={search_query}%3Arelevance&text={search_query.replace(' ', '%20')}"

        # Send an HTTP GET request using Selenium
        driver.get(url)

        # Wait for product titles to become available
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-title')))

        # Get the page source after JavaScript rendering
        page_source = driver.page_source

        # Extract and display product details
        soup = BeautifulSoup(page_source, 'html.parser')
        products = soup.find_all('div', class_='cp-product typ-plp')

        cheapest_product = None  # Initialize with None

        for product in products:
            # Extract product title
            title_element = product.find('h3', class_='product-title plp-prod-title').find('a')
            title = title_element.text.strip()

            # Extract product price
            price_element = product.find('span', class_='amount')
            price_str = price_element.text.strip() if price_element else "N/A"

            # Remove ₹ symbol and commas, then convert to an integer
            price = int(re.sub(r'[^\d]', '', price_str))

            # Compare the price with the cheapest product found so far
            if cheapest_product is None or price < cheapest_product["price"]:
                cheapest_product = {
                    "title": title,
                    "price": price,
                    "image_url": product.find('img')['data-src'],
                    "product_link": 'https://www.croma.com' + title_element['href']
                }

        if cheapest_product:
            print("Cheapest Product:")
            print(f"Title: {cheapest_product['title']}")
            print(f"Price: {cheapest_product['price']}")
            print(f"Image URL: {cheapest_product['image_url']}")
            print(f"Product Link: {cheapest_product['product_link']}")
        else:
            print(f"No results found on Croma for {name}.")

    except ScraperException as se:
        print(se)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        if driver is not None:
            driver.quit()  # Close the browser if it was opened

def main():
    product_name = input("Enter Product Name: ")
    croma(product_name)

if __name__ == "__main__":
    main()
