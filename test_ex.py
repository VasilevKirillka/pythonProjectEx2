import pytest
from playwright.sync_api import Page, sync_playwright
import openpyxl


@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page


def test_python(page: Page):
    file = openpyxl.Workbook()
    file.remove(file.active)
    sheet = file.create_sheet("Версии Python")
    sheet.append(["Release version", "Release date", "Download", "Release Notes"])

    page.goto('https://www.python.org/downloads/', timeout=60000)

    elements = page.query_selector_all('.download-list-widget .list-row-container li')

    for element in elements:
        release_number = element.query_selector('span.release-number').text_content()
        release_date = element.query_selector('span.release-date').text_content()
        release_download = element.query_selector('span.release-download a').get_attribute('href')
        release_enhancements = element.query_selector('span.release-enhancements a').get_attribute('href')

        sheet.append([release_number, release_date, release_download, release_enhancements])

    file.save('results.xlsx')
