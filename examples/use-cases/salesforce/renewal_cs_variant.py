"""
Salesforce Demo: Renewal/CS variant (Starter/free trial friendly)

What this file does:
- Demonstrates updating a renewal Opportunity and creating a task assigned to a teammate (CSM).

How it fits into browser-use:
- Shows a CSM-focused flow: update renewal fields and delegate follow-up tasks via the browser.
- Voice is NOT implemented; this script focuses only on browser actions.

Voice note (context only):
"For Acme Renewal, set ARR to 42k, stage Renewal Negotiation, next step ‘send order form’ by Friday; create task for CSM."

Automation:
- Preferred: Update renewal opportunity + assign task to teammate.
- Fallback: If renewal opportunities aren’t available, open the Account 'Acme' → add a Note with ARR=42k, Stage='Renewal Negotiation', Next Step='send order form by Friday' → create a Task for the CSM teammate due Friday.
"""

# @file purpose: Defines a demo Agent task to update a renewal Opportunity and assign a follow-up task to the CSM.

import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
    llm = ChatOpenAI(model="gpt-4.1-mini")

    task = (
        "In Salesforce (Starter/free trial friendly):"
        "\n1) Try opening the 'Acme Renewal' Opportunity; if not available, open the Account 'Acme'."
        "\n2) If the Opportunity exists, edit and set:"
        "\n   - ARR / Amount: 42000"
        "\n   - Stage: Renewal Negotiation"
        "\n   - Next Step: send order form by Friday"
        "\n3) Create a Task assigned to the CSM teammate: subject 'Send order form', due Friday, related to the same record."
        "\n4) If Opportunity is missing: add a Note on the Account with the same details (ARR 42k, Stage Renewal Negotiation, Next Step)."
        "\n5) Confirm updates and the task are visible on the record."
    )

    _, browser_session = ensure_debug_chrome_and_session(port=9222)
    await prompt_to_continue()

    agent = Agent(task=task, llm=llm, browser_session=browser_session)
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())


