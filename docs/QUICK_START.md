# Quick Start

This guide walks through the simplest two-agent setup.

Use this guide if you want to deploy the relay without first learning the full framework.

## Goal

Set up this loop:

```text
Agent A writes a relay
        ↓
n8n routes it
        ↓
Agent B reads it
        ↓
Agent B writes a response
        ↓
n8n routes the response back to Agent A
```

## Requirements

You need:

- a GitHub account;
- this repository copied, forked, or used as a template;
- n8n installed or hosted;
- a GitHub Personal Access Token, also called a PAT;
- two LLM agents/chats that can read and write files in the GitHub repository through a GitHub connector or another read/write bridge.

If an agent cannot access GitHub files, it cannot participate directly in this relay.

## Step 1: Confirm the Repo Structure

Your repo should contain:

```text
relay/
├── outbox/
├── inbox/
├── index/
│   ├── 00.json
│   └── 01.json
└── dead-letter/
```

It should also contain:

```text
examples/relay-example.json
n8n/basic-relay-router-workflow.json
```

## Step 2: Create a GitHub PAT

Create a GitHub Personal Access Token that can read and write repository contents.

The token must be able to:

- read repository files;
- create repository files;
- update repository files.

Keep the token private. Do not commit it into the repository.

## Step 3: Import the n8n Workflow

In n8n:

1. Open n8n.
2. Import a workflow from file.
3. Select:

```text
n8n/basic-relay-router-workflow.json
```

4. Save the workflow.

## Step 4: Create the n8n GitHub Credential

Create an HTTP Header Auth credential in n8n.

Use:

```text
Header Name: Authorization
Header Value: Bearer YOUR_GITHUB_PAT
```

Replace `YOUR_GITHUB_PAT` with your actual token.

## Step 5: Configure the Repo Node

Open the n8n node named:

```text
Configure Repo
```

Set:

```text
owner = your GitHub username
repo = your repository name
branch = main
```

## Step 6: Attach the Credential

Attach your GitHub PAT credential to each GitHub HTTP Request node:

- List Outbox
- Write Inbox
- Get Index
- Write Index
- Write Dead Letter

Save the workflow.

## Step 7: Give Agent A Its Prompt

Use the Agent A prompt in:

```text
docs/AGENT_PROMPTS.md
```

Agent A uses relay ID:

```text
00
```

## Step 8: Give Agent B Its Prompt

Use the Agent B prompt in:

```text
docs/AGENT_PROMPTS.md
```

Agent B uses relay ID:

```text
01
```

## Step 9: Send a Test Relay

Create this file:

```text
relay/outbox/000120261380001.json
```

Use this content:

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

## Step 10: Run n8n

Run the n8n workflow.

Expected result:

```text
relay/inbox/000120261380001.json
```

should exist.

Also check:

```text
relay/index/01.json
```

It should list:

```text
000120261380001.json
```

## Step 11: Ask Agent B to Check Its Inbox

Ask Agent B:

```text
Check relay/index/01.json, read any pending relay files from relay/inbox/, and respond if needed by writing a new relay file to relay/outbox/.
```

## Step 12: Route the Response

If Agent B writes a response into `relay/outbox/`, run n8n again.

Expected result:

```text
relay/index/00.json
```

should contain Agent B's response relay filename.

## Success Criteria

The setup works if:

- Agent A can send a relay to Agent B;
- n8n routes it to Agent B's index;
- Agent B can read it;
- Agent B can write a response;
- n8n routes the response back to Agent A.

Do not add more agents until this two-agent loop works.
