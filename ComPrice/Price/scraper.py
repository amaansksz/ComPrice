from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time 

def amazon(name):
    try:
        base_url = "https://www.amazon.in"
        search_url = f"{base_url}/s?k={name.replace(' ', '+')}"

        max_retries = 5
        product_list = []

        for retry in range(max_retries):
            try:
                # Initialize the Selenium WebDriver with a custom user agent
                chrome_options = ChromeOptions()
                chrome_options.headless = True
                chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")  # Replace with your desired user agent
                webdriver_path = r"C:\\Users\\Amaan Shaikh\\OneDrive - RizviCollegeOfEngineering\\Desktop\\Price Comparison\\Backend\\chromedriver-win64\\chromedriver.exe"
                service = ChromeService(executable_path=webdriver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)

                driver.get(search_url)

                # Wait for the page to load (you may need to customize the wait time)
                time.sleep(5)

                # Parse the page with BeautifulSoup
                soup = BeautifulSoup(driver.page_source, "html.parser")

                results = soup.find_all("div", {"data-component-type": "s-search-result"})

                for result in results:
                    title_elem = result.find("h2", class_="a-size-mini")
                    title = title_elem.get_text() if title_elem else "N/A"

                    # Check if the title contains the search query
                    if name.lower() not in title.lower():
                        continue

                    try:
                        price_elem = result.find("span", class_="a-price-whole")
                        # Convert price to an integer (remove currency symbol and commas)
                        price = float(price_elem.get_text().replace(",", "")) if price_elem else None
                    except (AttributeError, ValueError):
                        price = "N/A"

                    link_elem = result.find("a", class_="a-link-normal")
                    link = "https://www.amazon.in" + link_elem.get("href") if link_elem else "N/A"

                    # Extract image URL
                    try:
                        image_elem = result.find("img", class_="s-image")
                        image_url = image_elem.get("src") if image_elem else "N/A"
                    except (AttributeError, KeyError):
                        image_url = "N/A"

                    product_list.append({
                        "title": title,
                        "price": price,
                        "link": link,
                        "image_url": image_url,
                    })
                product_list = [product for product in product_list if name.lower() in product["title"].lower()]
                # Remove products with no price information
                product_list = [product for product in product_list if product["price"] is not None]

                # Sort the product list by price
                product_list.sort(key=lambda x: x["price"])
                product_list = [product for product in product_list if name.lower() in product["title"].lower()]
                return product_list[0]

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                time.sleep(2)  # Wait for a few seconds before retrying

            finally:
                if driver:
                    driver.quit()

        return "Max retries reached. Unable to retrieve data from Amazon."
    
    except:
        return "Error occurred while searching on Amazon."

def flipkart(name):
    try:
        base_url = "https://www.flipkart.com"
        search_url = f"{base_url}/search?q={name.replace(' ', '+')}"

        max_retries = 5
        product_list = []

        for retry in range(max_retries):
            try:
                # Initialize the Selenium WebDriver
                chrome_options = ChromeOptions()
                chrome_options.headless = True
                webdriver_path = r"C:\\Users\\Amaan Shaikh\\OneDrive - RizviCollegeOfEngineering\\Desktop\\Price Comparison\\Backend\\chromedriver-win64\\chromedriver.exe"  # Update with your chromedriver path
                service = ChromeService(executable_path=webdriver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)

                driver.get(search_url)

                # Wait for the page to load (you may need to customize the wait time)
                time.sleep(5)

                # Parse the page with BeautifulSoup
                soup = BeautifulSoup(driver.page_source, "html.parser")

                results = soup.find_all("div", {"class": "_1AtVbE"})

                for result in results:
                    title_elem = result.find("div", {"class": "_4rR01T"})
                    title = title_elem.get_text() if title_elem else "N/A"
                    # Check if the title contains the search query
                    if name.lower() not in title.lower():
                        continue
                    # After extracting titles, add a filter to match the exact search query
                    product_list = [product for product in product_list if name.lower() in product["title"].lower()]

                    try:
                        price_elem = result.find("div", {"class": "_30jeq3"})
                        # Convert price to an integer (remove currency symbol and commas)
                        price = float(price_elem.get_text().replace("₹", "").replace(",", "")) if price_elem else None
                    except (AttributeError, ValueError):
                        price = "N/A"

                    link_elem = result.find("a", {"class": "_1fQZEK"})
                    link = base_url + link_elem.get("href") if link_elem else "N/A"

                    # Extract image URL
                    try:
                        image_elem = result.find("img", {"class": "_396cs4"})
                        image_url = image_elem.get("src") if image_elem else "N/A"
                    except (AttributeError, KeyError):
                        image_url = "N/A"

                    product_list.append({
                        "title": title,
                        "price": price,
                        "link": link,
                        "image_url": image_url,
                    })
                product_list = [product for product in product_list if name.lower() in product["title"].lower()]
                # Remove products with no price information
                product_list = [product for product in product_list if product["price"] is not None]

                # Sort the product list by price
                product_list.sort(key=lambda x: x["price"])
                
                return product_list[0]

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                time.sleep(2)  # Wait for a few seconds before retrying

            finally:
                if driver:
                    driver.quit()

        return "Max retries reached. Unable to retrieve data from Flipkart."

    except:
        return "Error occurred while searching on Flipkart."


def croma(name):
    try:
        # Initialize the driver
        chrome_options = ChromeOptions()
        chrome_options.headless = True
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
        webdriver_path = r"C:\\Users\\Amaan Shaikh\\OneDrive - RizviCollegeOfEngineering\\Desktop\\Price Comparison\\Backend\\chromedriver-win64\\chromedriver.exe"
        service = ChromeService(executable_path=webdriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # URL of the Croma search results page with the search query
        search_query = name

        url = f"https://www.croma.com/searchB?q={search_query}%3Arelevance&text={search_query.replace(' ', '%20')}"

        # Send an HTTP GET request using Selenium
        driver.get(url)

        # Wait for product titles to become available
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-title')))

        # Get the page source after JavaScript rendering
        page_source = driver.page_source

        # Extract and display product details
        soup = BeautifulSoup(page_source, 'html.parser')
        products = soup.find_all('div', class_='cp-product typ-plp')
        time.sleep(5)
        cheapest_product = []  

        for product in products:
            # Extract product title
            title_element = product.find('h3', class_='product-title plp-prod-title').find('a')
            title = title_element.text.strip()
        # Check if the title contains the search query
            if name.lower() not in title.lower():
                continue
            # Extract product price
            price_element = product.find('span', class_='amount')
            price_str = price_element.text.strip() if price_element else "N/A"

            # Remove ₹ symbol and commas, then convert to an integer
            price = int(re.sub(r'[^\d]', '', price_str))
            
            cheapest_product.append({
            "title": title,
            "price": price,
            "link": 'https://www.croma.com' + title_element['href'],
            "image_url": product.find('img')['data-src'],
        })

        # Remove products with no price information
        cheapest_product = [product for product in cheapest_product if product["price"] is not None]
    
        # Sort the product list by price
        cheapest_product.sort(key=lambda x: x["price"])
    
        if cheapest_product:
            print("Cheapest Product:")
            print(f"Title: {cheapest_product[0]['title']}")
            print(f"Price: ₹{cheapest_product[0]['price']:.2f}")
            print(f"Image URL: {cheapest_product[0]['image_url']}")
            print(f"Product Link: {cheapest_product[0]['link']}")
        else:
            print("No results found.")
    except:
        return "product not found"
        # Close the browser
        if driver is not None:
            driver.quit()


def vijaysales(name):
    # Configure Selenium
    chrome_options = ChromeOptions()
    chrome_options.headless = True
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
    service = ChromeService(executable_path=r"C:\\Users\\Amaan Shaikh\\OneDrive - RizviCollegeOfEngineering\\Desktop\\Price Comparison\\Backend\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    search_query = name
    # Construct the search URL
    search_url = f"https://www.vijaysales.com/search/{search_query.replace(' ', '%20')}"

    # Send an HTTP GET request using Selenium
    driver.get(search_url)

    # Wait for JavaScript content to load
    driver.implicitly_wait(5)

    # Get the page source after JavaScript rendering
    page_source = driver.page_source
    time.sleep(5)  # Add some time to ensure page content is loaded

    soup = BeautifulSoup(page_source, 'html.parser')
    products = soup.find_all('div', class_='col5_2 Dynamic-Bucket-Main vj-sr-4per-row pb-bx-srch animate')

    cheapest_product = []

    for product in products:
        # Extract title
        title_element = product.find('h2', class_='Dynamic-Bucket-ProductName')
        title = title_element.text.strip()

        # Check if the title contains the search query
        if name.lower() not in title.lower():
            continue

        # Wait for the price element to be visible
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'Dynamic-Bucket-vsp'))
            )
        except:
            # Handle the case where price element is not found
            price_element = None

        # Extract price
        if price_element:
            price_text = price_element.text.strip()
            price = float(price_text.replace('₹', '').replace(',', ''))
        else:
            price = "N/A"

        # Extract image URL
        img_element = product.find('img', class_='img-responsive')
        img_url = img_element['data-original']

        # Extract product link
        link_element = product.find('a', class_='nabprod')
        product_link = link_element['href']

        cheapest_product.append({
            "title": title,
            "price": price,
            "link": product_link,
            "image_url": img_url,
        })

    # Remove products with no price information
    cheapest_product = [product for product in cheapest_product if product["price"] is not None]

    # Sort the product list by price
    cheapest_product.sort(key=lambda x: x["price"])

    if cheapest_product:
        n={
        print(f"Title: {cheapest_product[0]['title']}"),
        print(f"Price: ₹{cheapest_product[0]['price']:.2f}"),
        print(f"Image URL: {cheapest_product[0]['image_url']}"),
        print(f"Product Link: {cheapest_product[0]['link']}")}
        return n
    else:
        print("No results found.")

    # Close the browser
    driver.quit()


if __name__ == "__main__":
    product_name = input("Enter Product Name: ")



        # results
# amazon_results = amazon(product_name)
# if amazon_results != "Max retries reached. Unable to retrieve data from Amazon.":
    # print("Amazon Result:")
    # print(f"Title: {amazon_results['title']}")
    # print(f"Price: {amazon_results['price']}")
    # print(f"Link: {amazon_results['link']}")
    # print(f"Image URL: {amazon_results['image_url']}")
# else:
    # print(amazon_results)
# 
# flipkart_results = flipkart(product_name)
# if flipkart_results != "Max retries reached. Unable to retrieve data from Flipkart.":
    # print("Flipkart Result:")
    # print(f"Title: {flipkart_results['title']}")
    # print(f"Price: {flipkart_results['price']}")
    # print(f"Link: {flipkart_results['link']}")
    # print(f"Image URL: {flipkart_results['image_url']}")
# else:
    # print(flipkart_results)
croma_results= croma(product_name)
vijaysales_results=vijaysales(product_name)

