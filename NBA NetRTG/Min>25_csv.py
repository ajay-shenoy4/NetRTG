from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import os

# Setup WebDriver
service = Service("/Users/ajayshenoy/Downloads/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service)  # Ensure you have the ChromeDriver installed
url = "https://www.nba.com/stats/lineups/advanced"
driver.get(url)

# Define the folder path for saving CSV files
folder_path = os.path.join(os.getcwd(), "CSV Files")
os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

csv_file_path = os.path.join(folder_path, "table_data_filtered_25.csv")

try:
    # Wait for the table to load or an ad to appear
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "Crom_table__p1iZz"))
    )

    # Check and handle the ad if it appears
    try:
        ad_close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
        )
        ad_close_button.click()  # Click the ad's close button
        print("Ad closed successfully.")
    except Exception as ad_error:
        print("No ad detected or unable to close the ad:", ad_error)

    # Initialize data storage
    data = []
    column_names_added = False  # Track if column names are added

    # Counter for pages
    pages_scraped = 0

    while True:  # Continue scraping until MIN < 25 is encountered
        # Locate the table
        table = driver.find_element(By.CLASS_NAME, "Crom_table__p1iZz")
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Extract table headers (column names) if not already added
        if not column_names_added:
            header_row = rows[0]  # Assuming the first row contains headers
            headers = [header.text for header in header_row.find_elements(By.TAG_NAME, "th")]
            data.append(headers)
            column_names_added = True

        # Extract table data for the current page (skip the header row)
        for row in rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            
            # Get the value in the MIN column (4th column, index 3)
            min_value = float(cells[3].text) if cells[3].text else 0.0

            # Only add rows where MIN > 25
            if min_value > 25:
                data.append([cell.text for cell in cells])
            else:
                # Stop scraping when MIN < 25
                break

        # Check if we should stop scraping
        if min_value <= 25:
            break

        # Increment page counter
        pages_scraped += 1

        # Check if the "Next Page" button is available and clickable
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@title='Next Page Button']")
                )
            )
            if "disabled" in next_button.get_attribute("class"):
                break  # Exit loop if the "Next Page" button is disabled
            next_button.click()
            time.sleep(2)  # Allow the next page to load
            # Wait for the table to reload on the new page
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Crom_table__p1iZz"))
            )
        except Exception as e:
            print(f"Error navigating to next page: {e}")
            break  # Exit loop if "Next Page" button is not found

    # Save the filtered data to CSV inside the CSV Files folder
    with open(csv_file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"Data saved to {csv_file_path}")

finally:
    driver.quit()
