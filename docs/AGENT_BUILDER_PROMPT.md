# Agent Builder Prompt

Use this prompt with an LLM agent that has GitHub repository access.

The agent should build out the basic two-agent relay network files and stop whenever the user must complete a private/manual step.

Do not paste secrets into this prompt.

---

## Copy-Ready Prompt

```text
You are helping me set up RI-Git-Synched-Relays in a GitHub repository.

Your job is to build the basic two-agent relay network using GitHub files and n8n workflow files.

Scope:
- Set up a two-agent relay only.
- Agent A ID: 00.
- Agent B ID: 01.
- Use GitHub as the relay mailbox.
- Use n8n as the router.
- Use webhook-first routing.
- Do not add persistent memory.
- Do not add extra agents unless I explicitly ask later.
- Do not store or request my GitHub PAT.
- Do not write secrets into files.

Required repo files:
- relay/outbox/.gitkeep
- relay/inbox/.gitkeep
- relay/dead-letter/.gitkeep
- relay/index/00.json
- relay/index/01.json
- examples/relay-example.json
- n8n/basic-relay-router-webhook.json
- docs/AGENT_PROMPTS.md
- docs/QUICK_START.md
- docs/PRIVACY_AND_SECURITY.md

Index file contents:
relay/index/00.json:
{
  "agent": "00",
  "pending": [],
  "updated": null
}

relay/index/01.json:
{
  "agent": "01",
  "pending": [],
  "updated": null
}

Example relay contents:
{
  "relay_id": "000120261380001",
  "type": "relay",
  "from": "00",
  "to": "01",
  "task": "Smoke test",
  "message": "Confirm receipt only.",
  "context": null,
  "history": null,
  "timestamp": "2026-05-18T12:00:00Z",
  "status": "pending"
}

n8n workflow requirements:
- Start with a Webhook node.
- Accept GitHub push events.
- Detect changed files under relay/outbox/ ending in .json.
- Fetch the relay JSON from GitHub.
- Validate required fields: relay_id, from, to, task, message, timestamp, status.
- Treat only 00 and 01 as valid recipients.
- For valid relays:
  - write relay/inbox/{relay_id}.json
  - update relay/index/{to}.json by appending {relay_id}.json to pending if not already present
- For invalid relays:
  - write a JSON record to relay/dead-letter/
- Use placeholder GitHub credential references only.
- Do not include any real PAT or secret.

Agent prompt requirements:
Create docs/AGENT_PROMPTS.md with copy-ready prompts for Agent A and Agent B.
Each prompt must tell the agent:
- its relay ID;
- to read its own relay/index/{id}.json;
- to read pending files from relay/inbox/;
- to write outgoing relays to relay/outbox/;
- not to edit another agent's index directly;
- not to delete relay files;
- not to modify relay/inbox or relay/dead-letter directly.

User/manual steps:
When you reach a step that requires my private action, stop and ask me to complete it.
Do not try to do these actions for me unless I explicitly provide access and authorize it:
- creating my GitHub PAT;
- entering my PAT into n8n;
- connecting LLM agents to GitHub;
- activating n8n credentials;
- adding the n8n webhook URL to GitHub repository settings.

When stopping for user action, give me:
1. the exact place to go;
2. the exact value to paste;
3. the expected result;
4. what to say when I am done.

Privacy and safety requirements:
- Do not collect secrets.
- Do not ask me to paste a PAT into chat.
- Do not write tokens to repo files.
- Do not claim the setup is secure beyond what is actually true.
- State that users control their GitHub repo, n8n instance, LLM connectors, and data.

Output style:
- Keep steps short.
- Use plain language.
- Do one setup phase at a time.
- Do not give long explanations unless I ask.
- If a file is changed, list the file path and what changed.
- If something cannot be verified, say so plainly.

Start by checking whether the required files already exist in the repo.
Then create or update only the missing or incorrect files needed for the two-agent setup.
```

---

## Notes for Users

This prompt is intended for an LLM agent with Git access.

The agent can prepare repository files, but it should not handle your private token.

Your GitHub PAT belongs only in your own n8n credential field.

If the agent asks for your PAT in chat, stop and do not provide it.
