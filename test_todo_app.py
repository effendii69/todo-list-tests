import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture
def driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Commented out for debugging
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # To suppress GPU errors
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://localhost:3000")
    yield driver
    driver.quit()

def test_page_load(driver):
    assert "To Do List" in driver.title, "Page title does not match"

def test_page_title_consistency(driver):
    initial_title = driver.title
    task_input = driver.find_element(By.XPATH, "//form[@action='/']/input")
    task_input.send_keys("Title Test Task")
    button = driver.find_element(By.XPATH, "//form[@action='/']/button")
    button.click()
    time.sleep(10)  # Wait for page load
    WebDriverWait(driver, 60).until(lambda d: d.current_url == "http://localhost:3000/Today")
    assert driver.title == initial_title, "Page title changed after action"

def test_empty_task_validation(driver):
    task_input = driver.find_element(By.XPATH, "//form[@action='/']/input")
    task_input.clear()
    button = driver.find_element(By.XPATH, "//form[@action='/']/button")
    button.click()
    time.sleep(10)  # Wait for page load
    WebDriverWait(driver, 60).until(lambda d: d.current_url == "http://localhost:3000/Today")
    empty_items = driver.find_elements(By.XPATH, "//div[@class='item']/p[normalize-space()='']")
    assert len(empty_items) == 0, f"Empty task added, found {len(empty_items)} empty items"

def test_task_input_field_exists(driver):
    assert driver.find_element(By.XPATH, "//form[@action='/']/input").is_displayed(), "Task input field not found"
