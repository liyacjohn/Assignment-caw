from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json

# Setting up the Chrome WebDriver
driver = webdriver.Chrome()
driver.get("https://testpages.herokuapp.com/styled/tag/dynamic-table.html")

try:
    # Step 1: Click on the Table Data button using XPath
    table_data_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[3]/details/summary")))
    table_data_button.click()

    # Step 2: Input data into the text fields
    input_data = '[{"name": "Bob", "age": 20, "gender": "male"}, {"name": "George", "age": 42, "gender": "male"}, {"name": "Sara", "age": 42, "gender": "female"}, {"name": "Conor", "age": 40, "gender": "male"}, {"name": "Jennifer", "age": 42, "gender": "female"}]'

    input_text_field = driver.find_element(By.ID, "jsondata")
    input_text_field.clear()
    input_text_field.send_keys(input_data)

    caption_text_field = driver.find_element(By.ID, "caption")
    caption_text_field.clear()
    caption_text_field.send_keys("Dynamic Table")

    id_text_field = driver.find_element(By.ID, "tableid")
    id_text_field.clear()
    id_text_field.send_keys("dynamictable")

    # Click on Refresh Table button
    refresh_table_button = driver.find_element(By.ID, "refreshtable")
    refresh_table_button.click()

    # Step 3: Wait for the table to be updated
    table_rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#dynamictable tr")))

    expected_data = json.loads(input_data)
    for index, row in enumerate(table_rows[1:]):  # Skip the first row (header)
        columns = row.find_elements(By.TAG_NAME, "td")
        print(f"Row {index + 1} - Name: {columns[0].text}, Age: {columns[1].text}, Gender: {columns[2].text}")

        assert columns[0].text == expected_data[index]["name"]
        assert columns[1].text == str(expected_data[index]["age"])
        assert columns[2].text == expected_data[index]["gender"]

    print("Test passed successfully!")

except Exception as e:
    print(f"Test failed: {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
