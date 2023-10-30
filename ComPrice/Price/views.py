from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time 
import json


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
                time.sleep(2)

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
                if product_list:
                    return product_list[0]
                else:
                    return "Product not found on Amazon"
            except Exception as e:
                error_message = {"error":str(e)}
                time.sleep(2)  # Wait for a few seconds before retrying
                return json.dumps(error_message)
    finally:
        if driver:
            driver.quit()

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
                chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
                webdriver_path = r"C:\\Users\\Amaan Shaikh\\OneDrive - RizviCollegeOfEngineering\\Desktop\\Price Comparison\\Backend\\chromedriver-win64\\chromedriver.exe"  # Update with your chromedriver path
                service = ChromeService(executable_path=webdriver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)

                driver.get(search_url)

                # Wait for the page to load (you may need to customize the wait time)
                time.sleep(2)

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
                if product_list:
                    return product_list[0]
                else:
                    return "Product not found on Flipkart"
            except Exception as e:
                error_message = {"error":str(e)}
                time.sleep(2)  # Wait for a few seconds before retrying
                return json.dumps(error_message)
    finally:
        if driver:
            driver.quit()


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
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-title')))
        driver.implicitly_wait(10)
        # Get the page source after JavaScript rendering
        page_source = driver.page_source
        time.sleep(2)
        # Extract and display product details
        soup = BeautifulSoup(page_source, 'html.parser')
        products = soup.find_all('div', class_='cp-product typ-plp')

        cheapest_product = None  # Initialize with None

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

            # Compare the price with the cheapest product found so far
            if cheapest_product is None or price < cheapest_product["price"]:
                cheapest_product = {
                    "title": title,
                    "price": price,
                    "image_url": product.find('img')['data-src'],
                    "link": 'https://www.croma.com' + title_element['href']
                }
        if cheapest_product:
                    return cheapest_product
        else:
            return "Product not found on Croma"
    finally:
        if driver is not None:
            driver.quit()


def vijaysales(name):
    try:
        # Configure Selenium
        chrome_options = ChromeOptions()
        chrome_options.headless = True
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
        service = ChromeService(executable_path=r"C:\\Users\\Amaan Shaikh\\OneDrive - RizviCollegeOfEngineering\\Desktop\\Price Comparison\\Backend\\chromedriver-win64\\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        search_query=name
        # Construct the search URL
        search_url = f"https://www.vijaysales.com/search/{search_query}"
    
        # Send an HTTP GET request using Selenium
        driver.get(search_url)
    
        # Wait for JavaScript content to load (you may need to customize this)
        # Example: Wait for the product titles to become available
        driver.implicitly_wait(10)
    
        # Get the page source after JavaScript rendering
        page_source = driver.page_source
        time.sleep(2)
        soup = BeautifulSoup(page_source, 'html.parser')
        products = soup.find_all('div', class_='col5_2 Dynamic-Bucket-Main vj-sr-4per-row pb-bx-srch animate')
    
        cheapest_product = None  # Initialize with None
    
        for product in products:
            # Extract title
            title_element = product.find('h2', class_='Dynamic-Bucket-ProductName')
            title = title_element.text.strip()
    
            # Check if the title contains the search query
            if name.lower() not in title.lower():
                continue
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
            link = link_element['href']
    
            # Compare the price with the cheapest product found so far
            if cheapest_product is None or price < cheapest_product["price"]:
                cheapest_product = {
                    "title": title,
                    "price": price,
                    "image_url": img_url,
                    "link": link
                }
        if cheapest_product:
                    return cheapest_product
        else:
            return "Product not found on Croma"
    finally:
        if driver is not None:
            driver.quit()

def aboutus(request):
    return render(request, 'Price/aboutus.html')
def contactus(request):
    return render(request, 'Price/contactus.html')
def index(request):
    return render(request, 'Price/index.html')
def how(request):
    return render(request, 'Price/how.html')
def Search(request):
    return render(request, 'Price/Search.html')
def results(request):
    return render(request, 'Price/results.html')


@csrf_exempt
def search_product(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Call the scraper functions to search for the product
        amazon_result = amazon(query)
        flipkart_result = flipkart(query)
        vijaysales_result = vijaysales(query)
        croma_result = croma(query)

        # You can customize the response format as needed
        search_results = {
            'amazon_result': amazon_result,
            'flipkart_result': flipkart_result,
            'croma_result': croma_result,
            'vijaysales_result': vijaysales_result,
        }

        return render(request, 'Price/results.html', search_results)
    else:
        # Handle the case when the request method is not GET
        return JsonResponse({'error': 'Invalid request method'})
