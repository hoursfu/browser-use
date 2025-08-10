"""
Salesforce Demo: Security questionnaire workflow (Starter/free trial friendly)

What this file does:
- Demonstrates kicking off a security questionnaire workflow and updating Next Step, including creating a task with a portal link.

How it fits into browser-use:
- Shows an operational flow across vendor portal and Salesforce tasks/fields, executed purely via the browser.
- Voice is NOT implemented; this script focuses only on browser actions.

Voice note (context only):
"Kick off security questionnaire for Acme; due Friday; link to their portal; update Next Step accordingly."

Automation:
- Open vendor portal web form (or internal checklist) → create a Salesforce Task with the link and due date → update Next Step (as a field if available, or via a Note on the Account/Opportunity).
"""

# @file purpose: Defines a demo Agent task for starting a security questionnaire and updating Salesforce accordingly.

import asyncio
import os
import sys
from sf_utils import (  # type: ignore[import]
    ensure_debug_chrome_and_session,
    prompt_to_continue,
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent
from browser_use.llm.openai.chat import ChatOpenAI


async def main():
    llm = ChatOpenAI(model="gpt-4.1-mini")

    task = (
        "1) Open the vendor security portal for Acme (or the internal security questionnaire checklist)."
        "\n2) Capture the portal URL and any relevant request ID."
        "\n3) In Salesforce (Starter/free trial friendly), open the related record: Opportunity if present, else Account."
        "\n4) Create a Task: subject 'Security questionnaire', include the portal link in the description, due Friday, assign to me; relate to that record."
        "\n5) Update 'Next Step' on the same record: if the field exists, set it; otherwise, add a Note with 'Next Step: Send/Complete security questionnaire by Friday'."
        "\n6) Confirm the task and Next Step are visible on the record."
    )

    _, browser_session = ensure_debug_chrome_and_session(port=9222)
    await prompt_to_continue()

    agent = Agent(task=task, llm=llm, browser_session=browser_session)
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())


