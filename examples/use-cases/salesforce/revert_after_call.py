"""
Salesforce Demo: After-call → Update an Opportunity (Starter/free trial friendly)

What this file does:
- Defines a concise demo flow that updates selling details after a customer call.
- Primary path uses Opportunity fields; if your free trial (Salesforce Starter) does not expose Opportunities/Contact Roles, it falls back to Account/Contact + Notes/Tasks.

How it fits into browser-use:
- Shows a realistic CRM workflow powered by the `Agent` + `ChatOpenAI` loop, operating fully in the browser.
- Voice is NOT implemented; this script focuses only on browser actions.

Voice note (example context, not executed):
"Acme call: move to Negotiation, set amount 58k ARR, close date Oct 30. Next step: send security questionnaire by Friday. Add John Smith as Decision Maker. Log call and create a follow-up task for Tuesday."

Automation (choose what exists in your org):
- Preferred: Open Opportunity → update Stage/Amount/Close Date/Next Step → add Contact Role (Decision Maker) → Log a Call → Create Task.
- Fallback for Starter/free trial: Open Account 'Acme' → add/update related Contact 'John Smith' (set Title Decision Maker if available) → Log a Call on Account/Contact with summary → create a follow-up Task (due next Tuesday) → add a Note on the Account with the same details (acting as Next Step).
"""

# @file purpose: Defines a demo Agent task to update a Salesforce Opportunity after a call.

import asyncio
import os
import sys

# Ensure local import of browser_use
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# Also allow importing sibling utils in this folder directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sf_utils import (  # type: ignore[import]
    ensure_debug_chrome_and_session,
    prompt_to_continue,
)

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent
from browser_use.llm.openai.chat import ChatOpenAI


async def main():
    llm = ChatOpenAI(model="o3")

    # Only the browser actions; adjust object/field names to your SF layout as needed.
    task = (
        "1) Open Opportunity 'Netflix'."
        "2) Click the edit button to update the opportunity to the following:"
        "   - Stage (dropdown): Qualification"
        "   - Amount (text field): clear this field"
        "   - Next Step (text field): clear this field"
        "3) Click the blue save button."
        "4) Click the triangle button next to the first Contact Role person"
        "   - Click the delete button"
        # "\n4) Log a Call on the same opportunity page: title 'Customer call', include a brief summary with the details above; save."
        # "\n5) Create a follow-up Task for me due next Tuesday, subject 'Follow up: send questionnaire', related to the same record."
    )

    _, browser_session = ensure_debug_chrome_and_session(port=9222)
    await prompt_to_continue()

    agent = Agent(task=task, llm=llm, browser_session=browser_session)
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())


