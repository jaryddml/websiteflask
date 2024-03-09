import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BaseScraper:
    def __init__(self, search_query=""):
        self.search_query = search_query

    def get_url(self):
        raise NotImplementedError("Subclasses must implement get_url method")

    def scrape(self):
        raise NotImplementedError("Subclasses must implement scrape method")

class JMBullionScraper(BaseScraper):
    def __init__(self, search_query=""):
        super().__init__(search_query)
        self.home_url = "https://www.jmbullion.com"

    def get_url(self, page=1):
        if page == 1:
            return f"{self.home_url}/search/?q="
        else:
            # Adjusted to follow the pagination structure you provided
            return f"{self.home_url}/search/?q=#/?_=1&page={page}"

    def scrape(self):
        results = []
        page = 1

        display = Display(visible=1, size=(800, 600))
        display.start()
        driver = webdriver.Chrome()

        try:
            # Start by visiting the homepage to ensure session cookies are set
            driver.get(self.home_url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            while True:
                current_url = self.get_url(page)
                driver.get(current_url)
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product")))
        

                soup = BeautifulSoup(driver.page_source, "html.parser")
                products = soup.find_all("div", class_="product type-product status-publish hentry mainproductIn cat-product first instock")

                if not products:
                    print(f"No more products found at page {page}.")
                    break

                for product in products:
                    # Your original logic for parsing product details
                    # Make sure to adjust these selectors based on actual page structure
                    title = product.find("span", class_="title").get_text(strip=True)
                    price = product.find("span", class_="price").get_text(strip=True)
                    link = product.find("a", href=True)['href']
                    image = product.find("img")['src']

                    result = {
                        'title': title,
                        'price': price,
                        'link': self.home_url + link if not link.startswith(self.home_url) else link,
                        'image': image
                    }
                    results.append(result)

                pagination_table = driver.find_elements(By.CSS_SELECTOR, "table.pagination.top")
                if pagination_table:
                    next_button = pagination_table[0].find_elements(By.CSS_SELECTOR, "td.searchspring-next")
                    if next_button and "none" in next_button[0].get_attribute("style"):
                        print("Reached the last page.")
                        break

                page += 1

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            driver.quit()
            display.stop()

        return results


class APMEXScraper(BaseScraper):
    def __init__(self, search_query=""):
        super().__init__(search_query)
        self.base_url = "https://www.apmex.com"

    def get_url(self, page=1):
        start_offset = 80 * (page - 1)  # Calculate the start offset for pagination
        if page == 1:
            return f"{self.base_url}/search?&q="
        else:
            # URL adjusted for pagination using start offset
            return f"{self.base_url}/search?&q=*&rows=80&view=grid&version=V2&start={start_offset}"

    def scrape(self):
        results = []
        page = 1

        display = Display(visible=1, size=(1200, 1200))
        display.start()
        driver = webdriver.Chrome()

        try:
            driver.get(self.base_url)  # Optionally start at the base URL

            while True:
                current_url = self.get_url(page=page)
                print(f"Fetching {current_url}...")
                driver.get(current_url)
                
                try:
                    # Wait for the products to load on the page
                    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-essential")))
                except TimeoutException:
                    print("Timeout waiting for products to load. Ending scraping.")
                    break
                
                soup = BeautifulSoup(driver.page_source, "html.parser")
                products = soup.find_all("div", class_="product-essential")
                if not products:
                    print("No more products found. Ending scraping.")
                    break

                for product in products:
                    title_element = product.find("div", class_="mod-product-title")  # Adjust the class name as necessary
                    title = title_element.get_text(strip=True) if title_element else "Title Not Found"
                    
                    price_element = product.find("span", class_="price")  # Adjust the class name as necessary
                    price = price_element.get_text(strip=True) if price_element else "Price Not Found"
                    
                    link_element = product.find("a", class_="item-link")  # Adjust the class name as necessary
                    link = "https://www.apmex.com" + link_element['href'] if link_element else "Link Not Found"
                    
                    image_element = product.find("img", class_="lazy")  # Adjust the class name as necessary
                    image = image_element['src'] if image_element else "Image Not Found"
                    
                    result = {
                        'title': title,
                        'price': price,
                        'link': link,
                        'image': image
                    }
                    results.append(result)

                page += 1  # Increment page for next iteration

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            driver.quit()
            display.stop()

        return results


def main():
    search_query = input("Enter search query for bullion and coin websites: ")

    scraper_classes = {
        'jmbullion': JMBullionScraper,
        'apmex': APMEXScraper,
    }


    #The lines below are never executed when running normally. Left in for debug reasons. 
    aggregated_results = []
    for website, scraper_class in scraper_classes.items():
        scraper = scraper_class(search_query)
        results = scraper.scrape()
        if results:
            aggregated_results.extend(results)

   
    with open("scraped_results.json", "w") as f:
        json.dump(aggregated_results, f)
    print("Results saved to scraped_results.json")


if __name__ == "__main__":
    main()
