# Playwright Web Automation Framework

---

## Author
**Vimal Surani**  

---

## Project Overview
This project is a web automation framework built using **Playwright** and **Python**.  The framework focuses on automating testing processes such as functional testing.

---

## Features
- **Page Object Model (POM)**: A modular design separating the test scripts from page interaction logic.
- **Functional Testing**: Ensures correct application functionality across pages (e.g., login, sorting, and checkout).


---

## Project Structure

```bash
├── screenshots/                    # Directory for storing screenshots
├── videos/                         # Directory for storing video recordings of test executions
├── reports                         # Directory to store reports
├── pages/                          # Directory containing page object model (POM) classes
│   ├── cart_page.py                # Cart page POM
│   ├── checkout_page.py            # Checkout page POM
│   ├── inventory_page.py           # Inventory page POM
│   └── login_page.py               # Login page POM
├── tests/                          # Directory for test cases
│   └── test_functional.py          # Functional test cases
├── README.md                       # Project documentation
└── conftest.py                     # Configuration and fixtures for tests
```