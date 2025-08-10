"""
Salesforce Demo: Prospecting helper (from LinkedIn, Starter/free trial friendly)

What this file does:
- Demonstrates creating a CRM record from LinkedIn details. Preferred path creates a Lead; fallback creates a Contact under an Account when Leads aren't enabled in the free trial.
- Adds a follow-up task and optionally opens a sequencing tool to start a draft sequence.

How it fits into browser-use:
- Shows cross-site extraction (LinkedIn) followed by CRM creation (Salesforce), with optional Outreach/Salesloft draft initiation.
- Voice is NOT implemented; this script focuses only on browser actions.

Voice note (context only):
"Create a Lead for Jane Doe at Globex, title VP Ops. Add source LinkedIn. Create task: ‘Send intro sequence #2 tomorrow 9am.’"

Automation:
- Preferred: Create Lead (Name=Jane Doe, Company=Globex, Title=VP Ops, Lead Source=LinkedIn) → create follow-up task.
- Fallback: Ensure Account 'Globex' exists → create Contact 'Jane Doe' with Title 'VP Ops' under that Account → add a Note 'Source: LinkedIn' → create follow-up task.
"""

# @file purpose: Defines a demo Agent task to create a Salesforce Lead from LinkedIn context and add a follow-up task.

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
        "From an open LinkedIn profile tab:"
        "\n1) Extract Name (e.g., Jane Doe), Company (Globex), and Title (VP Ops)."
        "\n2) In Salesforce (Starter/free trial friendly):"
        "\n   - If Leads exist: create a Lead with those values; set Lead Source to 'LinkedIn'."
        "\n   - Else: ensure Account 'Globex' exists; create Contact 'Jane Doe' (Title 'VP Ops') under the Account; add a Note 'Source: LinkedIn'."
        "\n3) Create a Task related to the created record: subject 'Send intro sequence #2', due tomorrow at 9:00 AM (local), assign to me."
        "\n4) Optional: open Outreach or Salesloft and start a draft for 'intro sequence #2' for this person; leave draft ready."
        "\n5) Return to the record and confirm the task appears in related activities."
    )

    _, browser_session = ensure_debug_chrome_and_session(port=9222)
    await prompt_to_continue()

    agent = Agent(task=task, llm=llm, browser_session=browser_session)
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())


