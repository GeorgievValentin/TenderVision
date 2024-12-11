from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

BASE_URL = "https://app.eop.bg"


# Function to parse 'publish_date'
def parse_publish_date(publish_date_str):
    now = datetime.now()
    if "секунд" in publish_date_str:
        return now.date()
    elif "минута" in publish_date_str or "минути" in publish_date_str:
        return now.date()
    elif "час" in publish_date_str or "часа" in publish_date_str:
        hours_ago = int(publish_date_str.split()[1]) if publish_date_str.split()[1].isdigit() else 1
        return (now - timedelta(hours = hours_ago)).date()
    elif "ден" in publish_date_str or "дни" in publish_date_str:
        days_ago = int(publish_date_str.split()[1]) if publish_date_str.split()[1].isdigit() else 1
        return (now - timedelta(days = days_ago)).date()
    else:
        return now.date()


# Function to parse 'deadline'
def parse_deadline(deadline_str):
    try:
        return datetime.strptime(deadline_str.split(",")[0], "%d.%m.%Y").date()
    except ValueError:
        return None


# Function to scroll down using Page Down multiple times
def page_down(driver, times = 5):
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(times):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)  # Short delay to ensure the page updates


def scrape_tenders():
    # Uncomment the following lines to run in headless mode (background mode)
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU rendering
    options.add_argument('--no-sandbox')  # Sandbox security (useful in some environments)
    options.add_argument('--disable-dev-shm-usage')  # Prevent resource exhaustion
    driver = webdriver.Chrome(options=options)
    """

    # Configure WebDriver for normal mode
    service = Service()  # Add path to WebDriver executable if necessary
    driver = webdriver.Chrome(service = service)  # No headless mode
    driver.get(f"{BASE_URL}/today")
    time.sleep(5)  # Allow the page to load fully

    # Simulate mouse hover over the scrollbar
    print("Simulating hover over scrollbar...")
    scrollbar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ps__rail-y"))
    )
    ActionChains(driver).move_to_element(scrollbar).perform()
    time.sleep(1)  # Allow interaction to register

    scraped_unique_ids = set()
    tenders = []
    current_page = 1

    while True:
        try:
            print(f"Scraping page {current_page}...")
            # Scroll down using Page Down
            page_down(driver, times = 5)

            # Parse the current page
            soup = BeautifulSoup(driver.page_source, "html.parser")

            for item in soup.find_all("nx1-published-tender"):
                try:
                    unique_id = item.find_all("span", class_ = "text--grey40a break-word min-width-0")[1].text.strip()
                    if unique_id in scraped_unique_ids:
                        continue

                    scraped_unique_ids.add(unique_id)

                    # Extract other details
                    name = item.find("span",
                                     class_ = "text--14px text--black text--bold break-word min-width-0").text.strip()
                    organization = item.find("span", class_ = "text--grey40a break-word min-width-0").text.strip()
                    award_method = item.find("div", class_ = "text--black").text.strip()
                    deadline_raw = item.find("div", class_ = "text--black ng-star-inserted").text.strip()
                    deadline = parse_deadline(deadline_raw)
                    publish_date_raw = item.find_all("div", class_ = "text--black")[-1].text.strip()
                    publish_date = parse_publish_date(publish_date_raw)
                    details_link = BASE_URL + item.find("a")["href"]

                    tenders.append({
                        "name": name,
                        "organization": organization,
                        "unique_id": unique_id,
                        "award_method": award_method,
                        "deadline": deadline,
                        "publish_date": publish_date,
                        "details_link": details_link,
                    })
                except Exception as e:
                    print(f"Error extracting tender data: {e}")

            # Check for the next page button
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'pagination-button') and contains(@id, 'next-page-button')]"))
            )

            if next_button.is_displayed() and next_button.is_enabled():
                ActionChains(driver).move_to_element(next_button).click().perform()
                time.sleep(5)
                current_page += 1
            else:
                print("No next button found. Reached the last page.")
                break

        except Exception as e:
            print(f"Unexpected error navigating pages: {e}")
            break

    driver.quit()

    print(f"Total tenders scraped: {len(tenders)}")
    return tenders
