import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

class TestDynamicTable(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://testpages.herokuapp.com/styled/tag/dynamic-table.html"
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_dynamic_table(self):
        # Step 1: Access the URL
        self.driver.get(self.base_url)

        # Step 2: Click on the Table Data button
        table_data_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[3]/details/summary"))
        )
        table_data_button.click()

        # Step 3: Input data into the text fields
        input_data = '[{"name": "Bob", "age": 20, "gender": "male"}, {"name": "George", "age": 42, "gender": "male"}, {"name": "Sara", "age": 42, "gender": "female"}, {"name": "Conor", "age": 40, "gender": "male"}, {"name": "Jennifer", "age": 42, "gender": "female"}]'

        input_text_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'jsondata'))
        )
        input_text_field.clear()
        input_text_field.send_keys(input_data)

        # Introduce a short sleep to wait for the input to be processed (You can improve this using WebDriverWait)
        time.sleep(1)

        caption_text_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'caption'))
        )
        caption_text_field.clear()
        caption_text_field.send_keys("Dynamic Table")

        id_text_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'tableid'))
        )
        id_text_field.clear()
        id_text_field.send_keys("dynamictable")

        # Click on Refresh Table button
        refresh_table_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'refreshtable'))
        )
        refresh_table_button.click()

        # Wait for the table body to become visible
        table_body = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'dynamictable'))
        )

        # Step 4: Assert the data in the table
        expected_data = json.loads(input_data)
        rows = table_body.find_elements(By.TAG_NAME, 'tr')

        for expected_row in expected_data:
            # Check if the expected data is present in the table
            matching_row = None
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, 'td')
                if (
                    columns and
                    columns[0].text.strip() == expected_row["name"] and
                    columns[1].text.strip() == str(expected_row["age"]) and
                    columns[2].text.strip() == expected_row["gender"]
                ):
                    matching_row = row
                    break

            self.assertIsNotNone(matching_row, f"Row not found for {expected_row}")

            # Print the updated row and values
            print(f"Row {rows.index(matching_row) + 1} - Name: {expected_row['name']}, Age: {expected_row['age']}, Gender: {expected_row['gender']}")

        # Test Passed Message
        print("Test Passed: All rows are correctly displayed in the dynamic table.")

if __name__ == '__main__':
    unittest.main()
