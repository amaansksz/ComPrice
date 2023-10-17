from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time

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

# Usage
product_name = input("Enter Product Name: ")
flipkart_results = flipkart(product_name)
if flipkart_results != "Max retries reached. Unable to retrieve data from Flipkart.":
    print(f"Title: {flipkart_results['title']}")
    print(f"Price: {flipkart_results['price']}")
    print(f"Link: {flipkart_results['link']}")
    print(f"Image URL: {flipkart_results['image_url']}")
else:
    print(flipkart_results)
