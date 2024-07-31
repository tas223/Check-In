from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import base64


def calculateSleepTime(flight):
    """ Computes delay in seconds until user can be checked in.

    Args:
        flight (str): formatted flight departure time.

    Returns:
        int: seconds for process to sleep before launching check in process.
    """
    flightTime = datetime.strptime(flight, '%m-%d-%Y %H:%M')
    currentTime = datetime.now()
    delay = flightTime - currentTime
    timer = str(delay).split(',')

    if len(timer) < 2:
        return 0

    days = int(timer[0].split(" ")[0]) - 1
    timerBreakdown = datetime.strptime(timer[-1].strip(), "%H:%M:%S.%f")
    totalSeconds = (days * 86400) + (timerBreakdown.hour * 3600) + \
        (timerBreakdown.minute * 60) + timerBreakdown.second
    return totalSeconds


def closePopUp(driver):
    """Closes pop up messages that block view or prevent driver from interacting with web page.

    Args:
        driver (webdriver): chrome web driver created in launchCheckIn().
    """
    try:
        closeButton = driver.find_element(
            By.CSS_SELECTOR, '[aria-label="Close pop up"]')
        closeButton.click()
    except:
        pass


def launchCheckIn(confirmationCode, firstName, lastName):
    """
        Checks user in for flight using Chrome webdriver and downloads a PDF of boarding pass. 
        All args are strings that are collected in checkIn.py and retrieved from command line arguments.
    """

    try:
        PATH = "/Users/aishanisrikumar/chromeDriver/chromedriver"
        service = Service(PATH)
        options = webdriver.ChromeOptions()

        chromeDriver = webdriver.Chrome(service=service, options=options)
        chromeDriver.get(
            "https://www.southwest.com/air/check-in/?clk=HC_Prepare_1284_CTA1")

        code = chromeDriver.find_element(By.ID, "confirmationNumber")
        code.send_keys(confirmationCode)
        passengerFirstName = chromeDriver.find_element(
            By.ID, "passengerFirstName")
        passengerFirstName.send_keys(firstName)
        passengerLastName = chromeDriver.find_element(
            By.ID, "passengerLastName")
        passengerLastName.send_keys(lastName)

        submit = chromeDriver.find_element(By.ID, "form-mixin--submit-button")
        submit.send_keys(Keys.RETURN)

        while True:
            try:
                # Pop up messages can be closed immediately, but page must load before chromeDriver clicks Check In button
                closePopUp(chromeDriver)
                WebDriverWait(chromeDriver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit-button")))
                submit = chromeDriver.find_element(
                    By.CSS_SELECTOR, "button.submit-button")
                submit.click()

                # If most recent submit button was print, then save page with boarding passes as a PDF
                classes = submit.get_attribute("class")
                if "boarding-pass-options--button-print" in classes.split():
                    WebDriverWait(chromeDriver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Print"]')))
                    closePopUp(chromeDriver)

                    # preferCSSPageSize is needed to exclude website decorations and only include the boarding passes
                    boardingPassData = chromeDriver.execute_cdp_cmd(
                        'Page.printToPDF', {"preferCSSPageSize": True, "format": "letter"})
                    boardingPass = base64.b64decode(boardingPassData["data"])

                    # Optional: add file path to save boarding pass to
                    with open("southwest_boarding_pass.pdf", "wb") as file:
                        file.write(boardingPass)
                    file.close()
                    break

            except Exception as e:
                print(e)
                break

        chromeDriver.quit()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    """
        Do not directly run this script. This file is executed using checkIn.py, which retrieves flight information from user and launches script in its own session to prevent interruptions.
    """
    confirmationCode, firstName, lastName, flightInfo = sys.argv[1:]
    sleepTime = calculateSleepTime(flightInfo)
    time.sleep(sleepTime)
    launchCheckIn(confirmationCode, firstName, lastName)
