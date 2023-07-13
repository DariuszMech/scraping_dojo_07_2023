import jsonlines
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv

load_dotenv()

class QuoteScraper:
    def __init__(self, url, output_file):
        self.url = url
        self.output_file = output_file
        self.chrome_options = Options()
        # self.chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def scrape_quotes(self):
        # print("OPENING WEBSITE")
        self.driver.get(self.url)
        quotes = []
        # print("START SEARCHING")
        while True:            
            elements = self.driver.find_elements(By.CSS_SELECTOR, ".quote")
            if elements:
                # print("QUOTES FOUND:")
                for element in elements:
                    quote_text = element.find_element(By.CSS_SELECTOR, ".text").text
                    author = element.find_element(By.CSS_SELECTOR, ".author").text
                    tags = [tag.text for tag in element.find_elements(By.CSS_SELECTOR, ".tag")]
                    quote = {"text": quote_text, "by": author, "tags": tags}
                    quotes.append(quote)
                    # print(quote)

                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, ".pager .next")
                    if "disabled" in next_button.get_attribute("class"):
                        break
                    next_url = next_button.find_element(By.TAG_NAME, "a").get_attribute("href")
                    self.driver.get(next_url)
                    # print("GO TO THE NEXT PAGE")
                except NoSuchElementException:
                    # print("NO NEXT PAGE")
                    break

        # print("SEARCH COMPLETED")
        self.driver.quit()
        # print("WEBSITE CLOSED")
        self.save_quotes(quotes)
        # print("QUOTES SAVED IN FILE: " + self.output_file)

    def save_quotes(self, quotes):
        with jsonlines.open(self.output_file, mode="w") as writer:
            writer.write_all(quotes)