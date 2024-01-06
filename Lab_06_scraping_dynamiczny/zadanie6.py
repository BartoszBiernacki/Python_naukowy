from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
import json


def scrape() -> list:

    options = Options()
    options.add_experimental_option("detach", True)
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://progresja.com/wydarzenia/')
    driver.maximize_window()

    rodo_button = driver.find_element(
        By.CSS_SELECTOR,
        'button[class="js-accept uk-button uk-button-default uk-margin-small-left"]'
    )
    rodo_button.click()

    ################################################################
    # Scroll down page to load it's full content
    scroll_position = 0
    while True:
        start, stop = scroll_position, scroll_position+1000
        driver.execute_script(f"window.scrollTo({start}, {stop});")
        time.sleep(0.2)

        current_scroll_position = driver.execute_script(
            "return window.pageYOffset;"
        )

        if current_scroll_position == scroll_position:
            break  # Break if no more scrolling is possible

        scroll_position = current_scroll_position
    time.sleep(1)

    ################################################################
    # get data from boxes representing events
    data = []
    containers = driver.find_elements(By.CLASS_NAME, 'fs-grid-item-holder')
    for container in containers:

        day = container.find_element(By.CSS_SELECTOR, 'h2[class*="startdate"]')
        month = container.find_element(By.CSS_SELECTOR, 'h5[class*="month1"]')
        year = container.find_element(
            By.CSS_SELECTOR,
            'h5[class="uk-h5 uk-margin-small uk-margin-remove-bottom uk-text-center"]',
        )
        hour = container.find_element(
            By.CSS_SELECTOR,
            'h5[class="uk-h5 uk-margin-remove-vertical uk-text-center"]',
        )

        date_ = f'{day.text} {month.text} {year.text} {hour.text}'
        date_ = ' '.join(date_.split())

        band = container.find_element(
            By.CSS_SELECTOR,
            'a[class="el-link uk-link-reset"]',
        )
        band_ = band.text

        (
            ActionChains(driver)
            .key_down(Keys.CONTROL)
            .click(band)
            .key_up(Keys.CONTROL)
            .perform()
         )

        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        main_page = driver.current_window_handle
        driver.switch_to.window(driver.window_handles[1])

        panels = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'div[class*="uk-panel"]:has(span.smallbefore)')
            )
        )

        cena_ = ''
        for panel in panels:
            if "CENA:" in panel.text:
                cena_ = panel.text

        cena_ = (
            cena_
            .replace('CENA:\n', '')
            .replace(' *KOŃCOWA CENA MOŻE ZAWIERAĆ OPŁATĘ SERWISOWĄ', '')
        )

        info = f'{date_.ljust(25)} {cena_.ljust(15)} {band_}'
        data.append(info)
        print(info)

        driver.close()
        driver.switch_to.window(main_page)

    return data


def save_json(data: list, fdir: str) -> None:
    with open(fdir, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        print(f'{fdir} saved')

