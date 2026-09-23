import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options




# def search_wikipedia_for_selenium():
#     # Initialize the Chrome WebDriver
#     print("Launching browser...")
#     driver = webdriver.Chrome()

#     try:
#         # 1. Navigate to Wikipedia's homepage
#         print("Opening Wikipedia...")
#         driver.get("https://www.wikipedia.org/")

#         # 2. Locate the search bar using its ID
#         search_box = driver.find_element(By.ID, "searchInput")

#         # 3. Type our search term and hit ENTER
#         print("Searching for Selenium...")
#         search_box.send_keys("Selenium (software)")
#         search_box.send_keys(Keys.RETURN)

#         # Pause for 5 seconds so you can see the loaded page
#         print("Page loaded. Closing in 5 seconds...")
#         time.sleep(5)

#     except Exception as e:
#         print(f"An error occurred: {e}")
        
#     finally:
#         # 4. Close the browser and end the session
#         driver.quit()
#         print("Browser closed.")

if __name__ == "__main__":

    # 1. Point to your manual ChromeDriver installation
    service = Service(executable_path='/home/fha/bin/chromedriver')

    # 2. Point to your browser installation (to avoid snap/flatpak issues)
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"

    # 3. Launch the browser
    driver = webdriver.Chrome(service=service, options=options)

    print("Opening Wikipedia...") # print to terminal
    driver.get("https://www.wikipedia.com") # go to a webstie

    

    search_box = driver.find_element(By.ID, "searchInput") # find something

    search_box.send_keys("Selenium (software)")
    search_box.send_keys(Keys.RETURN)

    time.sleep(5)
    driver.quit()
    print("Browser closed.")

    # search_wikipedia_for_selenium() # function call