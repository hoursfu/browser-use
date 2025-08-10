"""
Salesforce Demo: Meeting recap → CRM + email (Starter/free trial friendly)

What this file does:
- Demonstrates composing an AI-written recap email in Gmail/Outlook web and logging the email + attaching notes in Salesforce.

How it fits into browser-use:
- Shows multi-app workflow: draft/send email in webmail, then log the email on the related CRM record (Opportunity preferred; Account/Contact fallback) and attach a note with the recap.
- Voice is NOT implemented; this script focuses only on browser actions.

Voice note (context only):
"Recap for Globex: summary + next steps. Email them and CC me; log the email and attach the call notes."

Automation:
- Compose Gmail/Outlook web with AI-written recap → send or leave as draft → Log an Email on the opportunity → attach transcript summary as a Note.
"""

# @file purpose: Defines a demo Agent task to send a meeting recap and log it in Salesforce with attached notes.

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
        "Using Gmail or Outlook web:"
        "\n1) Draft an email to the Globex stakeholders with a concise meeting recap (summary + next steps)."
        "\n   - CC my email (from environment if available) or leave a placeholder."
        "\n   - Keep it professional and action-oriented; save or send."
        "\n2) In Salesforce (Starter/free trial friendly), open the related record: use Opportunity if present, else Account or Contact."
        "\n3) Log an Email activity referencing the sent/drafted recap; include a brief summary."
        "\n4) Create a Note on the same record with the transcript/recap content (attach file if available)."
        "\n5) Confirm the activity timeline shows the logged email and note."
    )

    _, browser_session = ensure_debug_chrome_and_session(port=9222)
    await prompt_to_continue()

    agent = Agent(task=task, llm=llm, browser_session=browser_session)
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())


