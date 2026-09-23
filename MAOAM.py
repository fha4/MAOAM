import my_configs

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime

def convert_date_format(date_string):
    # Parse the input string based on its format (Day, Month DD, YYYY)
    # %A = Full weekday name, %B = Full month name, %d = Day of month, %Y = 4-digit year
    parsed_date = datetime.strptime(date_string, "%A, %B %d, %Y")
    
    # Format the parsed date to MM/DD/YYYY
    # %m = 2-digit month, %d = 2-digit day, %Y = 4-digit year
    formatted_date = parsed_date.strftime("%m/%d/%Y")
    
    return formatted_date


def scrape_meals(wait):
    bursley_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Bursley")))
    bursley_link.click() # Click the link

    daily_menu_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Daily Menu")))
    daily_menu_link.click() # Click the link

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

    # get rid of allergens (eggs, milk, peanuts, sesame)
    temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div/main/form/div/div[3]/div/div[1]/section/div[1]/div/button[4]")))
    temp_elt.click()
    temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div/main/form/div/div[3]/div/div[1]/section/div[1]/div/button[7]")))
    temp_elt.click()
    temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div/main/form/div/div[3]/div/div[1]/section/div[1]/div/button[9]")))
    temp_elt.click()
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
    print(f"Found {num_rows} items to process. Recording foods...")

    # PHASE 1: RECORD EVERY FOOD ITEM AND ITS INGREDIENTS
    recorded_foods = []
    
    for i in range(1, num_rows + 1):
        temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='itemPanel']/section/div[4]/table/tbody/tr[{i}]")))

        if ("cbo_nn_itemGroupRow" in temp_elt.get_attribute("class")):
            # It's a category header, expand it
            temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='itemPanel']/section/div[4]/table/tbody/tr[{i}]/td/div")))
            temp_elt.click()
        else:
            # It's a food item
            temp_elt = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='itemPanel']/section/div[4]/table/tbody/tr[{i}]/td[2]/a")))
            food_name = temp_elt.text.strip()
            
            # Click it to grab the ingredients early so we have them stored
            temp_elt.click()
            
            food_header = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cbo_nn_LabelHeader")))
            ingredients_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cbo_nn_LabelIngredients")))
            
            # Store the data as a dictionary
            recorded_foods.append({
                "name": food_name,
                "ingredients": ingredients_element.text
            })
            
            # Close the modal
            exit_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_nn_nutrition_close")))
            exit_button.click()
            wait.until(EC.invisibility_of_element_located((By.ID, "btn_nn_nutrition_close")))

    return recorded_foods


def let_user_pick_food():

    selected_foods = []    
    for food in recorded_foods:
        while True:
            choice = input(f"\nDo you want '{food['name']}'? (y = Yes, n = No, i = Ingredients): ").strip().lower()

            if choice in ['y', 'yes']:
                selected_foods.append(food['name'])
                print(f"Added '{food['name']}' to array.")
                break
            elif choice in ['n', 'no']:
                print(f"Skipped '{food['name']}'.")
                break
            elif choice in ['i', 'ingredients']:
                # Print the pre-recorded ingredients instead of using the browser
                print(f"\n--- {food['name']} ---")
                print(f"Ingredients: {food['ingredients']}\n")
            else:
                print("Invalid input. Please enter 'y', 'n', or 'i'.")

    print("\nSelected Foods Array:", selected_foods)
    return selected_foods


def fill_out_form(driver, selected_foods):

    driver.get("https://dining.umich.edu/secure-form-to-go-meal-form/")

    sign_in_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='post-972']/div/div/a")))
    sign_in_link.click()
    
    username_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='identifier']")))
    username_box.send_keys(my_configs.uniqname)
    username_box.send_keys(Keys.RETURN)

    password_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='credentials.passcode']")))
    password_box.send_keys(my_configs.password)
    password_box.send_keys(Keys.RETURN)

    input("lmk when you did the okta thing: ")

    # input first name
    first_name_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='field_qso6546']")))
    first_name_box.send_keys(my_configs.first_name)

    # input last name
    last_name_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='field_m5nar']")))
    last_name_box.send_keys(my_configs.last_name)
    
    # input phone number
    phone_number_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='field_q953886']")))
    phone_number_box.send_keys(my_configs.phone_number)
        
    # input UMID
    umid_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='field_9p56oa6']")))
    umid_box.send_keys(my_configs.umid)
    
    # input dining hall
    bursley_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='frm_radio_11238-0']/label")))
    bursley_button.click()

    # input meal type
    breakfast_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='frm_radio_11240-0']/label")))
    breakfast_button.click()

    # input date
    date_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='field_m849z56']")))
    date_box.send_keys(convert_date_format(target_date))

    # TODO: input time of meal

    # input that I have restrictions
    restrictions_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='frm_radio_11243-0']/label")))
    restrictions_button.click()

    # input my restrictions
    restrictions_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='field_p07df2']")))
    restrictions_box.send_keys(my_configs.restrictions)

    # input dine in vs carry out
    dine_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='frm_radio_11302-0']/label")))
    dine_in_button.click()

    # input entree
    entree_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='field_gui97z5']")))
    entree_box.send_keys(selected_foods)

    # input notes
    notes_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='field_e29dy56']")))
    notes_box.send_keys(my_configs.notes)
    
    input("lmk when you're ready to submit: ")
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='frm_field_11451_container']/div/input")))
    submit_button.click()


if __name__ == "__main__":

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
        
        # Ask the user for the date via the terminal
        target_date = input("\nEnter the date exactly as it appears on the page (e.g., 'Monday, September 7, 2026'): ")

        wait = WebDriverWait(driver, 15) # Wait up to 15 seconds for a link containing to be clickable

        recorded_foods = scrape_meals(wait)
        print("\nAll items recorded successfully! Now let's review them.\n")

        # # PHASE 2: ASK THE USER ABOUT EACH RECORDED ITEM
        selected_foods = let_user_pick_food()

        fill_out_form(driver, selected_foods)
        print(target_date)
        print("TIME dine-in @ bursley")
        print(selected_foods)

        time.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        driver.quit()
        print("Browser closed.")    