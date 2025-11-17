import time
import pytest
from utilities.data_access import read_sop_data
from pages.login_page import LoginPage
from pages.sop_proposer_page import SOPProposerPage
from pages.sop_recommender_page import SOPRecommenderPage
from pages.sop_approver_page import SOPApproverPage
from pages.sop_proposer_verapproval import SOPProposerApproval
from pages.sop_published import SOPPublishPage

# Load Excel data once
sop_data = read_sop_data("data/sop_data.xlsx")


@pytest.mark.parametrize("data", sop_data)
def test_sop_full_flow_ddt(driver, data):
    """Data-driven End-to-End SOP Flow using Excel"""

    login = LoginPage(driver)
    proposer = SOPProposerPage(driver)
    reviewer = SOPRecommenderPage(driver)
    approver = SOPApproverPage(driver)
    proposer_approval = SOPProposerApproval(driver)
    publisher = SOPPublishPage(driver)

    role = data["role"]
    username = data["username"]
    password = data["password"]
    sop_title = data["sop_title"]
    sop_file = data.get("file_path")

    print(f"\n🔹 Running step for {role} ({username})")

    if role == "Proposer":
        login.login(username, password)
        proposer.create_new_document(sop_title, sop_file)
        login.logout()

    elif role == "Recommender":
        login.login(username, password)
        reviewer.review_document(sop_title)
        login.logout()

    elif role == "Approver" :
        login.login(username, password)
        approver.open_and_approve_from_last_page(sop_title)
        login.logout()

    elif role == "Proposer_Verification":
        login.login(username, password)
        proposer_approval.open_and_approve(sop_title)
        login.logout()

    elif role == "Publisher":
        login.login(username, password)
        publisher.open_and_approve(sop_title)
        login.logout()

    else:
        pytest.skip(f"⚠️ Unknown role type: {role}")

    time.sleep(3)
