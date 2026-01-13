import pytest
from playwright.sync_api import sync_playwright
import random
import string

BASE_URL = "http://192.168.80.77:8080/signUp"

def signup_form(page, test_username, test_email):
        page.fill("input[name='username']", test_username)
        page.fill("input[name='email']", test_email)
        password_fields = page.locator("input[name='password']")
        password_fields.nth(0).fill("12345678")
        password_fields.nth(1).fill("12345678")
        page.fill('input[role="combobox"]', "Buyer")

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(BASE_URL)
        yield page
        browser.close()


test_username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@pytest.mark.parametrize("iteration,expected_status", [(0, 200), (1, 400)])
def test_signup_new_existing_username(iteration, expected_status, page):

    test_email = ''.join(random.choices(string.ascii_letters + string.digits, k=8))+"@gmail.com"

    signup_form(page, test_username, test_email)

    with page.expect_response("**/api/v1/users/addUser") as response_info:
        page.click("input[type='submit'][value='Sign Me Up']")

    response = response_info.value

    print(f"Iteration {iteration + 1} - URL: {response.url}, Status: {response.status}")

    assert response.status == expected_status, f"Expected {expected_status}, got {response.status}"


#this test should fail, as app allows to register with username that contains special symbols
@pytest.mark.parametrize("iteration,expected_status", [(0, 400)])
def test_signup_special_symbols_username(iteration, expected_status, page):

    test_username = ''.join(random.choices(string.punctuation, k=10))
    test_email = ''.join(random.choices(string.ascii_letters + string.digits, k=8))+"@gmail.com"

    signup_form(page, test_username, test_email)

    with page.expect_response("**/api/v1/users/addUser") as response_info:
            page.click("input[type='submit'][value='Sign Me Up']")

    response = response_info.value

    print(f"Iteration {iteration + 1} - URL: {response.url}, Status: {response.status}")

    assert response.status == expected_status, f"Expected {expected_status}, got {response.status}"


@pytest.mark.parametrize("iteration,expected_status", [(0, 200), (1, 200), (2, 200), (3, 200)])
def test_signup_min_max_username(iteration, expected_status, page):

    length_list = [6, 7, 19, 20] 
    length = length_list[iteration]

    test_username = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    test_email = ''.join(random.choices(string.ascii_letters + string.digits, k=8))+"@gmail.com"

    signup_form(page, test_username, test_email)

    with page.expect_response("**/api/v1/users/addUser") as response_info:
        page.click("input[type='submit'][value='Sign Me Up']")

    response = response_info.value

    print(f"Iteration {iteration + 1} - URL: {response.url}, Status: {response.status}")

    assert response.status == expected_status, f"Expected {expected_status}, got {response.status}"


@pytest.mark.parametrize("iteration", [0, 1, 2])
def test_short_long_username(iteration, page):
    length_list = [5, 21, 0] 

    length = length_list[iteration]
    test_username = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    test_email = ''.join(random.choices(string.ascii_letters + string.digits, k=8))+"@gmail.com"

    signup_form(page, test_username, test_email)

    page.click("input[type='submit'][value='Sign Me Up']")

    assert page.url.endswith("/signUp")


test_email = ''.join(random.choices(string.ascii_letters + string.digits, k=8))+"@gmail.com"

#2nd itteration in this test should fail as app allows to create new account with an existing username
@pytest.mark.parametrize("iteration,expected_status", [(0, 200), (1, 400)])
def test_signup_new_existing_emails(iteration, expected_status, page):

    
    test_username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    signup_form(page, test_username, test_email)

    with page.expect_response("**/api/v1/users/addUser") as response_info:
        page.click("input[type='submit'][value='Sign Me Up']")

    response = response_info.value

    print(f"Iteration {iteration + 1} - URL: {response.url}, Status: {response.status}")

    assert response.status == expected_status, f"Expected {expected_status}, got {response.status}"