# Quick Start

Use this page to get the two-agent relay working.

Do one box at a time.

Do not add more agents yet.

---

## What You Need

- GitHub account
- This repo copied or forked
- n8n installed or hosted
- GitHub PAT/token
- Two LLM agents that can read/write GitHub files

If the agent cannot access GitHub files, it cannot use this relay directly.

---

## 1. Import the n8n Workflow

In n8n, import this file:

```text
n8n/basic-relay-router-webhook.json
```

Expected result:

```text
Workflow appears in n8n.
```

---

## 2. Add Your GitHub Token to n8n

Create an n8n credential:

```text
Type: HTTP Header Auth
Header Name: Authorization
Header Value: Bearer YOUR_GITHUB_PAT
```

Do not put the PAT in GitHub files.

Expected result:

```text
n8n has a saved GitHub credential.
```

---

## 3. Set Your Repo Name

Open this n8n node:

```text
Filter Outbox Files
```

Set these values:

```text
owner = your GitHub username
repo = your repo name
branch = main
```

Expected result:

```text
n8n knows which repo to watch.
```

---

## 4. Attach the GitHub Credential

Attach your GitHub credential to these n8n nodes:

```text
Fetch Relay File
Write Inbox
Get Index
Write Index
Write Dead Letter
```

Expected result:

```text
All GitHub request nodes have credentials.
```

---

## 5. Turn On the Workflow

Activate the n8n workflow.

Open the webhook node.

Copy the production webhook URL.

Expected result:

```text
You have a webhook URL copied from n8n.
```

---

## 6. Add the Webhook to GitHub

In GitHub, open your repo.

Go to:

```text
Settings → Webhooks → Add webhook
```

Use:

```text
Payload URL: paste the n8n webhook URL
Content type: application/json
Secret: leave blank for first setup
Events: Just the push event
Active: checked
```

Save it.

Expected result:

```text
GitHub now calls n8n when the repo changes.
```

---

## 7. Give Agent A Its Prompt

Open:

```text
docs/AGENT_PROMPTS.md
```

Copy the Agent A prompt into Agent A.

Agent A is:

```text
00
```

Expected result:

```text
Agent A knows how to use relay/index/00.json.
```

---

## 8. Give Agent B Its Prompt

Open:

```text
docs/AGENT_PROMPTS.md
```

Copy the Agent B prompt into Agent B.

Agent B is:

```text
01
```

Expected result:

```text
Agent B knows how to use relay/index/01.json.
```

---

## 9. Send the Test Relay

Create this file in GitHub:

```text
relay/outbox/000120261380001.json
```

Paste this into it:

```json
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
```

Commit the file.

Expected result:

```text
GitHub triggers n8n automatically.
```

---

## 10. Check Agent B's Inbox

Look for this file:

```text
relay/inbox/000120261380001.json
```

Then check:

```text
relay/index/01.json
```

It should list:

```text
000120261380001.json
```

Expected result:

```text
Agent B has mail.
```

---

## 11. Ask Agent B to Respond

Tell Agent B:

```text
Check relay/index/01.json, read any pending relay files from relay/inbox/, and respond if needed by writing a new relay file to relay/outbox/.
```

Expected result:

```text
Agent B writes a response relay into relay/outbox/.
```

---

## 12. Check Agent A's Inbox

After Agent B writes its response, GitHub should trigger n8n again.

Check:

```text
relay/index/00.json
```

Expected result:

```text
Agent A has Agent B's response.
```

---

## Done

The relay works if:

```text
Agent A → Agent B → Agent A
```

works through GitHub and n8n.

Stop here until the two-agent loop is stable.

---

## If It Fails

Use the manual fallback workflow only for troubleshooting:

```text
n8n/basic-relay-router-workflow.json
```

Do not add more agents until the basic loop works.
