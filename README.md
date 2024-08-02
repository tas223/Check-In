# Southwest Check-In Service

This program prompts the user for their flight information in the terminal, checks them in as soon as check in opens, and downloads a PDF of their boarding pass. This Python project uses Selenium to automate the check in process and starts a new session with subprocess to allow the script to run in the background.

Usage
- Clone the repository
- Download the ChromeDriver version that matches your current version of Google Chrome
- If desired, specify the file name or path for the downloaded boarding pass
- Run the checkIn.py script with the command "python checkIn.py"
- Answer all questions in the terminal and receive confirmation that check in was scheduled
