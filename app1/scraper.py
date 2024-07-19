import time
import re
from io import StringIO
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By




class VisaScraper:
    """
    A class to orchestrate the visa scraping process.
    """

    def __init__(self, navigator, parser, saver):
        """
        Initializes the VisaScraper with a navigator, parser, and saver.

        Parameters:
            navigator (Navigator): An instance of the Navigator class.
            parser (Parser): An instance of the Parser class.
            saver (Saver): An instance of the Saver class.
        """
        self.navigator = navigator
        self.parser = parser
        self.saver = saver

    def run(self):
        """
        Runs the scraping process and saves the results.
        """
        try:
            # Navigate and scrape data from the website
            pages = self.navigator.navigate()
            for page in pages:
                self.parser.parse_page(page)

        finally:
            self.navigator.close_driver()

        # Save the scraped data to files
        self.saver.save_to_files(self.parser.get_target_programs())


class Navigator:
    """
    A class responsible for navigating through the web pages.
    """

    def __init__(self, base_url):
        """
        Initializes the Navigator with the base URL and sets up the WebDriver.

        Parameters:
            base_url (str): The base URL of the website to scrape.
        """
        self.base_url = base_url

    def init_driver(self):
        """
        Initializes the Selenium WebDriver with desired options.

        Returns:
            WebDriver: The configured WebDriver instance.
        """
        options = webdriver.ChromeOptions()
        # (Optional) Add arguments to customize Chrome behavior

        driver = webdriver.Chrome(options=options)
        return driver

    def navigate(self):
        """
        Navigates through the pages and collects their sources.

        Returns:
            list: A list of page sources.
        """
        page_sources = []
        page_number = 1
        driver = self.init_driver()

        # Navigate to the initial page
        driver.get(self.base_url)

        while True:
            # Allow some time for the page to load fully
            time.sleep(12)

            # Collect the page source
            page_sources.append(driver.page_source)
            print(f"{page_number} Page Processed")

            # Find the "Next" button element by CSS selector
            next_buttons = driver.find_elements(By.CSS_SELECTOR, ".pagination > li > a")
            next_button = next(
                (btn for btn in next_buttons if btn.text.strip() == "Next" and "disabled" not in btn.get_attribute("class")),
                None,
            )

            if next_button:
                # Click the "Next" button and increment the page number
                page_number += 1
                next_button.click()
            else:
                # Break the loop if the "Next" button is disabled or not found
                break

        driver.quit()
        return page_sources

    def close_driver(self):
        """
        Closes the WebDriver.
        """
        pass  # Driver is closed in navigate()

class Parser:
    """
    A class responsible for parsing the web pages and extracting data.
    """

    def __init__(self):
        """
        Initializes the Parser with a dictionary to store target programs.
        """
        self.target_programs = {
            "186": [],
            "189": [],
            "190": [],
            "494": [],
            "485": [],
            "407": [],
            "187": [],
            "491": [],
            "482 Medium term stream": [],
            "482 Short term stream": [],
            "489 state or territory nominated": [],
        }

    def extract_visa_codes(self, visa_description):
        """
        Helper function to extract unique numeric visa codes from the visa descriptions.

        Parameters:
            visa_description (str): The description of the visas.

        Returns:
            str: A comma-separated string of unique visa codes.
        """
        # Use regex to find all unique three-digit numbers in the visa description
        return ", ".join(set(re.findall(r"\b\d{3}\b", visa_description)))

    def parse_page(self, page_source):
        """
        Parses data from a single page source and updates the target_programs dictionary.

        Parameters:
            page_source (str): The HTML source of the page.
        """
        # Wrap the HTML content in a StringIO object
        html_buffer = StringIO(page_source)
        # Read the HTML table directly using Pandas
        parsed_tables = pd.read_html(html_buffer)
        table = parsed_tables[0]

        # Keep only the "Occupation" and "Visa" columns
        table = table[["Occupation", "Visa"]]
        # Remove rows with undefined occupations
        table = table[table["Occupation"] != "undefined"]
        # Reset the index of the DataFrame
        table.reset_index(drop=True, inplace=True)

        # Extract visa codes from the "Visa" column
        table["Visa"] = table["Visa"].apply(lambda x: self.extract_visa_codes(x) if pd.notna(x) else "")

        # Iterate through the DataFrame and update the target_programs dictionary
        for index, row in table.iterrows():
            job_title = row["Occupation"].strip()  # Clean up job title
            visa_codes = row["Visa"].split(", ") if pd.notna(row["Visa"]) else []

            # Assign each job to the appropriate visa program
            for visa_code in visa_codes:
                if visa_code in self.target_programs:
                    self.target_programs[visa_code].append(job_title)

    def get_target_programs(self):
        """
        Returns the target programs dictionary.

        Returns:
            dict: The dictionary of target programs.
        """
        return self.target_programs


class Saver:
    """
    A class responsible for saving the extracted data to files.
    """

    def save_to_files(self, target_programs):
        """
        Saves the data for each program in a separate text file.

        Parameters:
            target_programs (dict): The dictionary of target programs.
        """
        # Iterate through the target programs and save each to a file
        for program, jobs in target_programs.items():
            filename = f"{program}.txt"
            with open(filename, "w") as file:
                # Write each job title to the corresponding file
                for job in jobs:
                    file.write(job + "\n")


if __name__ == "__main__":
    # Define the base URL
    base_url = "https://immi.homeaffairs.gov.au/visas/working-in-australia/skill-occupation-list"

    # Create instances of Navigator, Parser, and Saver
    navigator = Navigator(base_url)
    parser = Parser()
    saver = Saver()

    # Create a VisaScraper instance and run the scraper
    scraper = VisaScraper(navigator, parser, saver)
    scraper.run()
