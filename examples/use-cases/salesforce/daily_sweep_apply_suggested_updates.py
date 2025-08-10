"""
Salesforce Demo: Daily sweep → apply suggested updates (Starter/free trial friendly)

What this file does:
- Demonstrates reviewing a queue of transcripts/notes and applying suggested updates to Salesforce records with minimal clicks.

How it fits into browser-use:
- Shows a review-then-apply loop in the browser; each item shows a summary card to confirm, then applies changes to Salesforce.
- Voice is NOT implemented; this script focuses only on browser actions.

Voice note (context only):
"Apply suggested updates from yesterday’s meetings."

Automation:
- For each transcript in the queue, show a review card → one-click apply to Salesforce.
"""

# @file purpose: Defines a demo Agent task for a daily sweep applying suggested CRM updates from a queue of transcripts.

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
        "In a browser tab with a 'Suggested Updates' queue (internal tool or shared dashboard):"
        "\n1) For each item summarizing a CRM change (Opportunity preferred; Account/Contact fallback), open a review card and confirm."
        "\n2) Apply the change in Salesforce (Starter/free trial friendly) — update fields where available; otherwise add Notes/Tasks — then mark the item as done."
        "\n3) Continue until the queue is empty or the first 10 items are processed."
        "\n4) Produce a brief summary of applied updates."
    )

    _, browser_session = ensure_debug_chrome_and_session(port=9222)
    await prompt_to_continue()

    agent = Agent(task=task, llm=llm, browser_session=browser_session)
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())


