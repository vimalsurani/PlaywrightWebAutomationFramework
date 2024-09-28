# Playwright Web Automation Framework

---

## Author
**Vimal Surani**  

---

## Project Overview

This project is a web automation framework built using **Playwright** and **Python**. The framework focuses on automating testing processes such as functional testing, accessibility testing using axe-core, and visual regression testing using screenshot comparison. It also includes **Allure** reporting for better insights and documentation of test results.

---

## Features
- **Page Object Model (POM)**: A modular design separating the test scripts from page interaction logic.
- **Functional Testing**: Ensures correct application functionality across pages (e.g., login, sorting, and checkout).
- **Accessibility Testing**: Uses axe-core to verify that the application meets accessibility standards.
- **Visual Regression Testing**: Captures screenshots and compares them to baseline images for visual accuracy.
- **Allure Reports**: Generates detailed test execution reports for better visibility of test outcomes.

---

## Project Structure

```bash
├── data_regression/                # Directory for data regression files
├── screenshots/                    # Directory for storing screenshots
├── videos/                         # Directory for storing video recordings of test executions
├── reports                         # Directory to store reports
├── pages/                          # Directory containing page object model (POM) classes
│   ├── cart_page.py                # Cart page POM
│   ├── checkout_page.py            # Checkout page POM
│   ├── inventory_page.py           # Inventory page POM
│   └── login_page.py               # Login page POM
├── tests/                          # Directory for test cases
│   ├── test_accessibility.py       # Accessibility testing scripts
│   ├── test_visual.py              # Visual regression testing scripts
│   └── test_functional.py          # Functional test cases
├── requirements.txt                # Python dependencies
├── pytest.ini                      # Pytest configuration file
├── README.md                       # Project documentation
└── conftest.py                     # Configuration and fixtures for tests
```

## Setup Instructions

### Prerequisites

Before setting up the framework, ensure the following prerequisites are met:

- **Python**: Version 3.7 or later.
- **Node.js**: Required for Playwright installation.
- **pip**: Python package manager.
- **Playwright Browsers**: Chromium, Firefox, or Webkit. Installed through Playwright.
- **Google Chrome/Chromium**: Recommended for browser testing.
- **Allure**: For generating test reports (optional).

### Dependencies

You can install the necessary dependencies using the provided `requirements.txt` file. Here’s a list of dependencies used in the project

- `pytest`: Test framework for Python
- `pytest-regressions`: For data regression comparisons (used in visual testing).
- `playwright`: End-to-end testing framework.
- `allure-pytest`: For generating test reports.
- `pytest-playwright`: Pytest integration for Playwright.


### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vimalsurani/PlaywrightWebAutomationFramework.git
   cd PlaywrightWebAutomationFramework
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install  # Install browsers for Playwright
   ```
---

## Running the Tests

1. **Run all tests**:
   - Running Tests in Headed Mode (Default)
     ```bash 
     pytest -v
     ```
   - Running Tests in Headless Mode
     ```bash
     pytest -v --headless
     ```

2. **Run with Allure report generation**:
   ```bash
   pytest --alluredir=reports/allure_results
   allure serve reports/allure_results 
   ```

3. **Run specific tests**:
   - Functional tests:
     ```bash
     pytest -m functional
     ```
   - Accessibility tests:
     ```bash
     pytest -m accessibility
     ```
   - Visual regression tests:
     ```bash
     pytest -m visual
     ```
---

## Visual Regression Testing

Screenshots of pages are stored in the `screenshots` folder. You can compare new screenshots to baselines using `pytest-regressions`.

---

## Accessibility Testing

The framework uses the **axe-core** library to perform accessibility checks. Violations are reported in the test output and attached to Allure reports.

---

## Reporting with Allure

After running the tests, you can generate and view Allure reports using:

```bash
allure serve reports/allure_results
```

This will serve a detailed report in your default web browser.

---

For a **freestyle Jenkins job**, you can follow the steps below. This guide is tailored to set up Jenkins to run Playwright tests, generate Allure reports, and use the `batch` script for running the tests and generating the reports.

---

## Jenkins Setup (Freestyle Job)

This guide walks through setting up a Jenkins freestyle job to run Playwright tests and generate Allure reports.

## Prerequisites

1. **Jenkins**: Ensure Jenkins is installed and running.
2. **Python**: Ensure Python is installed on the machine where Jenkins is running.
3. **Node.js**: Install Node.js, as Playwright depends on it.
4. **Allure Commandline**: Install Allure Commandline for generating reports.
5. **Jenkins Plugins**:
   - **Allure Jenkins Plugin**
   - **HTML Publisher Plugin**
   - **NodeJS Plugin**

### Step 1: Install Required Jenkins Plugins

1. Open Jenkins dashboard.
2. Navigate to **Manage Jenkins > Manage Plugins > Available**.
3. Search for the following plugins and install them:
   - **Allure Jenkins Plugin**
   - **HTML Publisher Plugin**
   - **NodeJS Plugin**

### Step 2: Configure Global Tools in Jenkins

#### Configure Allure Commandline

1. Go to **Manage Jenkins > Global Tool Configuration**.
2. Scroll down to the **Allure Commandline** section.
3. Click **Add Allure Commandline**, provide a name like `Allure`, and specify the path where Allure is installed.
4. Save the configuration.

#### Configure Node.js in Jenkins

1. Go to **Manage Jenkins > Global Tool Configuration**.
2. Scroll to the **NodeJS** section.
3. Add a new NodeJS installation by providing a name (e.g., `NodeJS`) and selecting the Node.js version.
4. Save the configuration.

### Step 3: Create a Freestyle Job

1. On the Jenkins dashboard, click **New Item**.
2. Select **Freestyle project**, provide a job name (e.g., `Playwright_Automation_Job`), and click **OK**.
3. In the **General** section, you can add a brief description of the job.

### Step 4: Configure Build Steps

1. **Add Build Step**: Click on **Add build step** and select **Execute Windows batch command** (or **Execute shell** for Linux).
2. **Batch Command**:
   - Paste the following script, which installs dependencies, runs tests, and generates Allure reports:

   ```batch
   @echo off

   :: Set the Python path and Node.js path (if needed)
    set "SCRIPTS_PATH=%PYTHON_PATH%\Scripts"
    set PATH=%PATH%;%PYTHON_PATH%;%SCRIPTS_PATH%;%NODE_PATH%

   :: Install project dependencies
   pip install -r requirements.txt
   playwright install

   :: Run tests and generate Allure results
   pytest --alluredir=allure-results

   :: Generate Allure report if results exist
   if exist "allure-results" (
       echo "Generating Allure report..."
       allure generate allure-results -c -o allure-report
       echo "Allure report generated."
   ) else (
       echo "No allure-results found. Skipping report generation."
   )

   exit /b 0
   ```

### Step 5: Add Post-Build Action for Allure Report

1. Scroll down to **Post-build Actions**.
2. Click **Add post-build action** and select **Allure Report**.
3. In the **Allure Results** field, provide the path to the results (e.g., `allure-results`).
4. Save the configuration.

### Step 6: Run the Jenkins Job

1. Go back to the Jenkins dashboard.
2. Select your freestyle job.
3. Click **Build Now** to run the job.
4. Once the job completes, you can see the Allure report by clicking on the **Allure Report** link in the job page.

---