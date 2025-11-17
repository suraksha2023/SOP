import os
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def snap(driver, step_name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("screenshots", exist_ok=True)
    file_path = os.path.join("screenshots", f"{step_name}_{timestamp}.png")
    driver.save_screenshot(file_path)
    print(f"📸 Screenshot: {file_path}")


class SOPApproverPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def open_and_approve_from_last_page(self, title):
        """Goes to Under-Review Docs, jumps to last page (2nd last pagination button),
        finds the SOP document by title, and approves it."""
        driver = self.driver

        # Step 1️⃣ - Navigate to Under Review Docs
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@class='switch-menu']"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@class='bi bi-file-earmark-text nav-icon']"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Under-Review Docs']"))).click()
        snap(driver, "under_review_docs_opened")

        time.sleep(2)

        # Step 2️⃣ - Locate pagination and click second-last page
        pagination = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.pagination")))
        driver.execute_script("arguments[0].scrollIntoView(true);", pagination)
        time.sleep(1)

        # Find all clickable numbered page links
        page_links = pagination.find_elements(By.XPATH, ".//li[not(contains(@class,'disabled'))]/a")

        if len(page_links) < 2:
            print("⚠️ Only one page found, staying on current page.")
        else:
            # Click second-last link (the last numeric page)
            last_page_link = page_links[-2]
            driver.execute_script("arguments[0].scrollIntoView(true);", last_page_link)
            driver.execute_script("arguments[0].click();", last_page_link)
            print("➡️ Navigated to the last page of pagination.")
            time.sleep(3)

        snap(driver, "last_page_opened")

        # Step 3️⃣ - Try to locate document with given title
        try:
            sop_doc = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//a[normalize-space(text())='{title}']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", sop_doc)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", sop_doc)
            print(f"📄 Opened document titled: {title}")
            snap(driver, "sop_document_opened")
        except:
            print(f"❌ Document titled '{title}' not found on the last page.")
            return

        # Step 4️⃣ - Approve flow
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        approve_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Approve')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", approve_btn)
        driver.execute_script("arguments[0].click();", approve_btn)
        snap(driver, "approve_button_clicked")

        # Tick confirmation and OK button
        tick = self.wait.until(EC.element_to_be_clickable((By.ID, "accept_doc")))
        tick.click()
        ok_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "acceptToProposer")))
        ok_btn.click()
        snap(driver, "approval_popup_closed")

        print(f"✅ SOP '{title}' approved successfully!")
