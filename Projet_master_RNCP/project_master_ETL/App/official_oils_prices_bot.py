from selenium import webdriver
# import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_url_for_download_official_oils_prices():
    print("[INFO] Starting bot process for get download official oils prices URL")
    go_time = time.time()
    chrome_options = Options()

    # decomment for see navigation in real
    # chrome_options.add_argument("--headless")

    # Initialise solanium driver
    driver = webdriver.Chrome(options=chrome_options)
    # use undetected_chromedriver if we want discretion
    # driver = uc.Chrome(options=chrome_options)

    WebDriverWait(driver, 10)
    driver.get("https://www.ecologie.gouv.fr/politiques-publiques/prix-produits-petroliers")
    time.sleep(3)

    # remove popup for cookie
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tarteaucitronCTAButton.tarteaucitronDeny"))
    ).click()

    # click on "demarré" button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
                By.CSS_SELECTOR,"a.use-ajax.fr-btn[href^='/ajax/simulator/load/customer_simulator_energies_fuel_block']"))
    ).click()

    # click on "Étape suivante" button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Étape suivante']"))
    ).click()

    # time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[.//span[contains(normalize-space(.), 'Carburants routiers')]]"))
    ).click()

    # click on radio "suivre l evolution"
    radio = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='radio'][value='monitor']"))
    )
    driver.execute_script("arguments[0].click();", radio)

    # click on button for validate formulary ("étape suivante")
    next_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.webform-button--next"))
    )
    driver.execute_script("arguments[0].click();", next_btn)

    # choose all carburants in list
    label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for^='edit-monitor-road-fuels-gazole']"))
    )
    driver.execute_script("arguments[0].click();", label)
    label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for^='edit-monitor-road-fuels-sp95']"))
    )
    driver.execute_script("arguments[0].click();", label)
    label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for^='edit-monitor-road-fuels-sp95-e10']"))
    )
    driver.execute_script("arguments[0].click();", label)
    label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for^='edit-monitor-road-fuels-sp98']"))
    )
    driver.execute_script("arguments[0].click();", label)
    label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for^='edit-monitor-road-fuels-superethanol-e85']"))
    )
    driver.execute_script("arguments[0].click();", label)
    label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for^='edit-monitor-road-fuels-gpl']"))
    )
    driver.execute_script("arguments[0].click();", label)

    #full input starting data dates
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='monitor_start_date']"))
    ).send_keys("01011900")

    #full input ending data dates
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='monitor_end_date']"))
    ).send_keys("01012100")

    time.sleep(1)
    #click on "Soumettre" button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Soumettre']"))
    ).click()

    # wait response and get link for download data
    download_link = WebDriverWait(driver, 120).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.fr-col-none:last-child div.fr-download > a.fr-link--download"))
    ).get_attribute("href")
    print("[INFO] Download link scrapping by bot:", download_link)

    print("[INFO] Bot result in", time.time() - go_time)
    return download_link