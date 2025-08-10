"""
Salesforce Demo: Opportunity risk/update from transcript (Starter/free trial friendly)

What this file does:
- Demonstrates updating competitor info and adding a note to an Opportunity based on meeting transcript insights.

How it fits into browser-use:
- Shows how to apply extracted insights to CRM fields and related lists via the browser.
- Voice is NOT implemented; this script focuses only on browser actions.

Voice note (context only):
"Customer mentioned competitor WidgetCo and budget approved for Q4. Add competitor and note 'budget approved'."

Automation:
- Preferred: Update Opportunity Competitors related list; add note.
- Fallback: If Opportunities/Competitors aren’t available, open the Account and add a Note: "Competitor: WidgetCo; Budget approved for Q4".
"""

# @file purpose: Defines a demo Agent task to add competitor and budget-approved note on an Opportunity from transcript insights.

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
        "\n1) Try to open the related Opportunity; if not available, open its Account."
        "\n2) If Opportunity + Competitors related list exist: add 'WidgetCo' (create competitor if needed)."
        "\n3) Add a Note: 'Budget approved for Q4' on the same record."
        "\n4) If Opportunity/Competitors are missing: add a Note on the Account: 'Competitor: WidgetCo; Budget approved for Q4'."
        "\n5) Confirm the updates/notes are visible."
    )

    _, browser_session = ensure_debug_chrome_and_session(port=9222)
    await prompt_to_continue()

    agent = Agent(task=task, llm=llm, browser_session=browser_session)
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())


