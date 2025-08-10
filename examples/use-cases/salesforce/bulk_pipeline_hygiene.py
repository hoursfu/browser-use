"""
Salesforce Demo: Bulk pipeline hygiene (Starter/free trial friendly)

What this file does:
- Demonstrates a list-view-driven cleanup. Primary path uses Opportunity list views; fallback path uses Accounts when Opportunities aren't available in the free trial.

How it fits into browser-use:
- Uses the Agent to navigate list views, apply filters, iterate records, and perform updates via Tasks/Notes when bulk edit or fields are missing.
- Voice is NOT implemented; this script focuses only on browser actions.

Voice note (context only):
"Clean up opps: any Discovery stage with no activity in 30 days → set Next Step to ‘Re-engage email’ and create a task for me next Monday."

Automation:
- Preferred: Opportunity list view → filter to Stage=Discovery and no activity in 30 days → bulk-edit Next Step to 'Re-engage email' → create tasks per record.
- Fallback: Accounts list view → filter Last Activity older than 30 days → for each Account, create a Task (due next Monday) with subject 'Re-engage email' and add a Note saying Next Step='Re-engage email'.
"""

# @file purpose: Defines a demo Agent task for bulk pipeline hygiene via a Salesforce list view.

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
        "\n1) Try opening the Opportunities list view (e.g., 'All Open Opportunities'). If not available, open the Accounts list view."
        "\n2) If Opportunities exist: filter Stage='Discovery' and Last Activity older than 30 days (or equivalent)."
        "\n   - Bulk-edit Next Step to 'Re-engage email' and apply."
        "\n   - Then create Tasks per record: subject 'Re-engage email', due next Monday, assign to me."
        "\n3) If using Accounts instead: filter Last Activity older than 30 days. For each Account:"
        "\n   - Create a Task: subject 'Re-engage email', due next Monday, assign to me."
        "\n   - Add a Note on the Account with 'Next Step: Re-engage email'."
        "\n4) Spot-check a couple of records to confirm updates."
    )

    _, browser_session = ensure_debug_chrome_and_session(port=9222)
    await prompt_to_continue()

    agent = Agent(task=task, llm=llm, browser_session=browser_session)
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())


