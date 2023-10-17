from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Function to extract and find the cheapest product
def vijaysales(driver,page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    products = soup.find_all('div', class_='col5_2 Dynamic-Bucket-Main vj-sr-4per-row pb-bx-srch animate')

    cheapest_product = None  # Initialize with None

    for product in products:
        # Extract title
        title_element = product.find('h2', class_='Dynamic-Bucket-ProductName')
        title = title_element.text.strip()

        # Wait for the price element to be visible
        price_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'Dynamic-Bucket-vsp'))
        )

        # Extract price
        price_text = price_element.text.strip()
        price = float(price_text.replace('₹', '').replace(',', ''))

        # Extract image URL
        img_element = product.find('img', class_='img-responsive')
        img_url = img_element['data-original']

        # Extract product link
        link_element = product.find('a', class_='nabprod')
        product_link = link_element['href']

        # Compare the price with the cheapest product found so far
        if cheapest_product is None or price < cheapest_product["price"]:
            cheapest_product = {
                "title": title,
                "price": price,
                "image_url": img_url,
                "product_link": product_link
            }

    return cheapest_product


def main():
    # Take the product search query from the user
    search_query = input("Enter the product you want to search for: ")
    
    # Construct the search URL
    search_url = f"https://www.vijaysales.com/search/{search_query}"
    
    # Configure Selenium
    chrome_options = ChromeOptions()
    chrome_options.headless = True
    service = ChromeService(executable_path=r"C:\\Users\\Amaan Shaikh\\OneDrive - RizviCollegeOfEngineering\\Desktop\\Price Comparison\\Backend\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Send an HTTP GET request using Selenium
    driver.get(search_url)
    
    # Wait for JavaScript content to load (you may need to customize this)
    # Example: Wait for the product titles to become available
    driver.implicitly_wait(10)
    
    # Get the page source after JavaScript rendering
    page_source = driver.page_source
    
    # Extract and get the cheapest product
    cheapest_product = vijaysales(page_source)
    
    # Close the browser
    driver.quit()

    if cheapest_product:
        print("Cheapest Product:")
        print(f"Title: {cheapest_product['title']}")
        print(f"Price: ₹{cheapest_product['price']:.2f}")
        print(f"Image URL: {cheapest_product['image_url']}")
        print(f"Product Link: {cheapest_product['product_link']}")
    else:
        print("No results found.")

if __name__ == "__main__":
    main()