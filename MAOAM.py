import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 1. Point to your manual ChromeDriver installation
service = Service(executable_path='/home/fha/bin/chromedriver')

# 2. Point to your browser installation (to avoid snap/flatpak issues)
options = Options()
options.binary_location = "/usr/bin/google-chrome"

# 3. Launch the browser
driver = webdriver.Chrome(service=service, options=options)

print("Navigating to NetNutrition...")
driver.get("https://fss.studentlife.umich.edu/NetNutrition/1")

try:
    
    wait = WebDriverWait(driver, 15) # Wait up to 15 seconds for a link containing to be clickable
    bursley_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Bursley")))
    bursley_link.click() # Click the link

    wait = WebDriverWait(driver, 15) # Wait up to 15 seconds for a link containing to be clickable
    daily_menu_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Daily Menu")))
    daily_menu_link.click() # Click the link

    # Ask the user for the date via the terminal
    target_date = input("\nEnter the date exactly as it appears on the page (e.g., 'Monday, September 7, 2026'): ")

    # select date
    date_selector_xpath = "//*[@id='dropdownDateButton']"
    date_selector_button = wait.until(EC.element_to_be_clickable((By.XPATH, date_selector_xpath)))
    date_selector_button.click()
    print("Successfully clicked on date selector!")    
    # click on date
    date_link = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='nav-date-selector']/div/a[@title='{target_date}']")))
    print(f"Clicking on date: {date_link.text}")
    date_link.click()

    # select meal type
    mealType_selector_xpath = "//*[@id='dropdownMealButton']"
    mealType_selector_button = wait.until(EC.element_to_be_clickable((By.XPATH, mealType_selector_xpath)))
    mealType_selector_button.click()
    print("Successfully clicked on meal type selector!")
    # click on meal type
    mealType_link = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='nav-meal-selector']/div/a[@title='Breakfast']")))
    print(f"Clicking on date: {mealType_link.text}")
    mealType_link.click()

    # get rid of eggs
    temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div/main/form/div/div[3]/div/div[1]/section/div[1]/div/button[4]")))
    temp_elt.click()

    # get rid of milk
    temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div/main/form/div/div[3]/div/div[1]/section/div[1]/div/button[7]")))
    temp_elt.click()

    # get rid of peanuts
    temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div/main/form/div/div[3]/div/div[1]/section/div[1]/div/button[9]")))
    temp_elt.click()

    # get rid of sesame
    temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div/main/form/div/div[3]/div/div[1]/section/div[1]/div/button[11]")))
    temp_elt.click()

    # do some weird stuff to make sure the table has updated (pt. 1)
    first_row_xpath = "//*[@id='itemPanel']/section/div[4]/table/tbody/tr[1]"
    old_first_row = wait.until(EC.presence_of_element_located((By.XPATH, first_row_xpath)))

    # get rid of tree nuts
    temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div/main/form/div/div[3]/div/div[1]/section/div[1]/div/button[14]")))
    temp_elt.click()

    # do some weird stuff to make sure the table has updated (pt. 2)
    print("Waiting for the table to update...")
    wait.until(EC.staleness_of(old_first_row))
    time.sleep(3)
    print("Table updated!")

    current_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='itemPanel']/section/div[4]/table/tbody/tr")))
    num_rows = len(current_rows)
    print(f"Found {num_rows} items to process.")

    selected_foods = []    
    for i in range(1, num_rows + 1):

        temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='itemPanel']/section/div[4]/table/tbody/tr[{i}]")))

        if ("cbo_nn_itemGroupRow" in temp_elt.get_attribute("class")):
            temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='itemPanel']/section/div[4]/table/tbody/tr[{i}]/td/div")))
            temp_elt.click()

        else:

            temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='itemPanel']/section/div[4]/table/tbody/tr[{i}]/td[2]/a")))
            food_name = temp_elt.text.strip()

            print("where we at 1")

            temp_elt.click()

            while True:
                choice = input(f"\nDo you want '{food_name}'? (y = Yes, n = No, i = Ingredients): ").strip().lower()

                if choice in ['y', 'yes']:
                    selected_foods.append(food_name)
                    print(f"Added '{food_name}' to array.")
                    break
                elif choice in ['n', 'no']:
                    print(f"Skipped '{food_name}'.")
                    break
                elif choice in ['i', 'ingredients']:
                    # Re-locate and click to view ingredients modal
                    
                    food = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cbo_nn_LabelHeader")))
                    ingredients = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cbo_nn_LabelIngredients")))

                    print(f"\n--- {food.text} ---")
                    print(f"Ingredients: {ingredients.text}\n")

                    

                else:
                    print("Invalid input. Please enter 'y', 'n', or 'i'.")


            # find x button, then leave
            exit_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_nn_nutrition_close")))
            exit_button.click()
            wait.until(EC.invisibility_of_element_located((By.ID, "btn_nn_nutrition_close")))

    print("\nSelected Foods Array:", selected_foods)














    time.sleep(15)




    

    
    # # This XPath looks for the table row containing your date, then finds the 'Breakfast' link inside that same row.
    # # Note: If the site's HTML layout is div-based rather than table-based, 'ancestor::tr' might need to be changed to 'ancestor::div'.
    # breakfast_xpath = f"//*[contains(text(), '{target_date}')]/ancestor::div//a[contains(text(), 'Breakfast')]"

    
    

    
    


    
    # # 6. Click on the "Eggs" button on the side of the screen
    # print("Looking for the 'Eggs' category...")
    # eggs_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Eggs")))
    # eggs_link.click()
    # print("Successfully clicked on Eggs!")



    
    # # Pause so you can visually verify it worked before closing
    # time.sleep(5)




except Exception as e:
    print(f"An error occurred: {e}")
    
finally:
    driver.quit()
    print("Browser closed.")
    # print("Program finished.")









# driver.get("https://dining.umich.edu/secure-form-to-go-meal-form/") # go to a website
# time.sleep(100)

# try:
    
#     search_box = driver.find_element(By.ID, "searchInput") # find something

# except Exception as e:
#     print(f"An error occurred: {e}")
    
# finally:
#     print("\n")


# time.sleep(15)
# driver.quit()
# print("Browser closed.")













