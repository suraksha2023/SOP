import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def snap(driver, step_name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("screenshots", exist_ok=True)
    file_path = os.path.join("screenshots", f"{step_name}_{timestamp}.png")
    driver.save_screenshot(file_path)
    print(f"📸 Screenshot saved: {file_path}")

class SOPRecommenderPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def find_document_across_pages(self, title):
        try:
            pagination = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.pagination")))
        except:
            # No pagination block found, assume single page with documents
            try:
                sop_doc = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f"//a[normalize-space(text())='{title}']")))
                return sop_doc
            except:
                return None

        # Collect all page number links (excluding Disabled, Next, Prev)
        page_links = pagination.find_elements(By.XPATH,
                                              ".//li[contains(@class,'page-item') and not(contains(@class,'disabled'))]//a[not(contains(text(),'Next')) and not(contains(text(),'Prev'))]")

        for page_link in page_links:
            # Scroll into view before clicking (helps avoid click interception)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", page_link)
            page_number = page_link.text.strip()
            print(f"Checking page {page_number}")
            try:
                page_link.click()
            except Exception as e:
                print(f"Click failed for page {page_number}: {e}")
                # Try JS click if normal click fails
                self.driver.execute_script("arguments[0].click();", page_link)

            # Wait for page load (replace with smarter wait if needed)
            time.sleep(2)

            # Try finding document on this page
            try:
                sop_doc = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f"//a[normalize-space(text())='{title}']")))
                print(f"Found document on page {page_number}")
                return sop_doc
            except:
                # Not found on this page; continue to next
                continue

        # Document not found on any page
        return None

    def review_document(self, title):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@class='switch-menu']"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@class='bi bi-file-earmark-text nav-icon']"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Under-Review Docs']"))).click()
        snap(self.driver, "review_docs_opened")

        sop_doc = self.find_document_across_pages(title)
        if sop_doc is None:
            print(f"❌ Document with title '{title}' not found across all pages.")
            return

        self.driver.execute_script("arguments[0].click();", sop_doc)
        snap(self.driver, "sop_opened")

        # Scroll full page down before interacting with submit button
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Allow scrolling animation

        # Wait and scroll submit button into view
        submit_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Approve')]")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(1)  # Allow any scroll animation to complete
        submit_btn.click()
        snap(self.driver, "approved")

        tick = self.wait.until(EC.element_to_be_clickable((By.ID, "accept_doc")))
        tick.click()

        ok_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "acceptToApprover")))
        ok_btn.click()
        snap(self.driver, "popup_closed")

        print("✅ SOP reviewed successfully")