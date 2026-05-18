# RI-Git-Synched-Relays

**R**outing **I**nfrastructure for **Git-Synchronized Relays**

## Foreword

I know very little coding, by way of trying to make a game and getting tired of copy and pasting relays between numerous agents I decided to see what there was for a work around. Maybe there was one already and I didn't know what to look it up as, but as far as I could tell this didn't exist already, or nobody thought to use it this way. I used ChatGPT and Claude alternatively to build it. This was my work around, I didn't code it, I directed its building. So there very likely are tweaks that can improve it. I hope this helps someone create something amazing, or something that makes them feel amazing for having accomplished something. Everything that follows was CGPT written.

— WA-Ladd

## Overview

This project describes a simple relay pattern for passing structured messages between LLM agents using GitHub as a shared mailbox, with n8n handling the boring routing work.

The core idea is:

- A message is written as a JSON file.
- The JSON file has a known sender, recipient, task, and message.
- n8n detects new relay files and routes them.
- A receiving agent can read the relay through a GitHub connector.
- A response can be written back as another JSON relay.
- n8n moves valid relays to inbox/index locations and sends invalid relays to dead-letter.

The relay format is the important part. The specific model provider is not.

Any LLM that can read and write files in the same GitHub repository can participate.

## Why n8n Matters

The relay pattern can be tested manually, but it is much less convenient without automation.

Without n8n, the human still has to:

- notice that a new relay exists;
- copy or move it to the correct inbox;
- update the recipient index;
- handle invalid recipients;
- repeat the process for responses.

With n8n, the human can mostly stay out of the middle. n8n can watch the repo, read relay files, route them, update indexes, and send bad relays to dead-letter.

A manual relay is good for understanding the pattern. An n8n workflow is what makes the pattern useful day to day.

## What This Is

This is a minimal communication layer for LLM-assisted workflows.

It is useful when:

- you want two AI agents to pass tasks between each other;
- you do not want to manually copy and paste every relay;
- you want a visible record of what was sent;
- you want a simple Git-based structure instead of a full orchestration platform;
- you want n8n or a similar workflow tool to handle routing.

## What This Is Not

This is not:

- a complete agent framework;
- a private memory system;
- a security system;
- a replacement for judgment or validation;
- a production-ready automation platform by itself.

Do not put private logs, API keys, personal records, or sensitive project material in a public relay repository.

## Minimal Repository Structure

```text
relay-repo/
├── README.md
├── relay/
│   ├── outbox/
│   ├── inbox/
│   ├── index/
│   │   ├── 00.json
│   │   └── 01.json
│   └── dead-letter/
└── examples/
    └── relay-example.json
```

## Agent IDs and Counters

For a bare-bones setup, use two agents:

```text
00 = Agent A
01 = Agent B
```

Each sender should maintain its own sequence counter for relay IDs.

That means Agent A and Agent B do not share one global counter. Agent A counts its own outgoing relays, and Agent B counts its own outgoing relays.

Example:

```text
Agent A sends first relay to Agent B:
000120261380001

Agent A sends second relay to Agent B:
000120261380002

Agent B sends first relay back to Agent A:
010020261380001

Agent B sends second relay back to Agent A:
010020261380002
```

Breakdown:

```text
000120261380001
00    sender: Agent A
01    recipient: Agent B
2026  year
138   Julian day
0001  Agent A's outgoing counter
```

```text
010020261380001
01    sender: Agent B
00    recipient: Agent A
2026  year
138   Julian day
0001  Agent B's outgoing counter
```

So both agents can have a `0001` relay on the same day because the counter belongs to the sender.

The important rule is:

```text
Counter uniqueness is per sender, not global.
```

## Relay JSON Format

Each relay is a JSON file.

Example:

```json
{
  "relay_id": "000120261380001",
  "type": "relay",
  "from": "00",
  "to": "01",
  "task": "Review this plan",
  "message": "Please review this plan for gaps, risks, or unclear instructions.",
  "context": null,
  "history": null,
  "timestamp": "2026-05-18T12:00:00Z",
  "status": "pending"
}
```

## Field Meanings

| Field | Meaning |
|---|---|
| `relay_id` | Unique ID for this relay |
| `type` | Message type, usually `relay` |
| `from` | Sender ID |
| `to` | Recipient ID |
| `task` | Short description of the request |
| `message` | Main body of the relay |
| `context` | Optional reference to another file |
| `history` | Optional previous relay/session reference |
| `timestamp` | ISO timestamp |
| `status` | Usually `pending` for active relay files |

## Basic Message Flow

```text
Agent A writes relay/outbox/000120261380001.json
        ↓
n8n detects the outbox file
        ↓
n8n checks the relay JSON
        ↓
n8n writes/copies it to relay/inbox/
        ↓
n8n updates relay/index/01.json
        ↓
Agent B reads relay/index/01.json
        ↓
Agent B opens the listed relay file
        ↓
Agent B writes a response relay back to relay/outbox/
        ↓
n8n routes the response back to Agent A
```

## Index Files

Each receiving agent can have an index file listing pending messages.

Example:

```json
{
  "agent": "01",
  "pending": [
    "000120261380001.json"
  ],
  "updated": "2026-05-18T12:00:00Z"
}
```

This lets an agent or interface check one small file instead of scanning the whole inbox.

## Dead Letter Folder

Invalid relays can be sent to:

```text
relay/dead-letter/
```

This is useful when:

- the `to` field is missing;
- the recipient ID does not exist;
- the JSON is malformed;
- routing cannot safely continue.

## Bare-Bones GitHub Setup

### 1. Create a New GitHub Repository

Create a new repo that does not contain private logs or project history.

### 2. Add the Folder Structure

Create:

```text
relay/outbox/
relay/inbox/
relay/index/
relay/dead-letter/
examples/
```

GitHub does not track empty folders, so add placeholder files if needed:

```text
.gitkeep
```

### 3. Add Index Files

Create:

```text
relay/index/00.json
relay/index/01.json
```

`relay/index/00.json`:

```json
{
  "agent": "00",
  "pending": [],
  "updated": null
}
```

`relay/index/01.json`:

```json
{
  "agent": "01",
  "pending": [],
  "updated": null
}
```

### 4. Give Both LLMs Access to the Repo

Each LLM needs a GitHub connector or some other way to inspect repository files.

At minimum:

- Agent A can write a relay file.
- Agent B can read relay/index and relay/inbox.
- Agent B can write a response relay.
- Agent A can read the response.

For early testing, this can be done manually through GitHub's web editor.

## Bare-Bones n8n Setup

n8n is the practical router.

A minimal n8n workflow needs these parts:

1. **Trigger**
   - GitHub webhook, scheduled poll, or manual test trigger.
   - Detect new or changed files in `relay/outbox/`.

2. **Fetch Relay File**
   - Read the JSON file from GitHub.

3. **Parse Relay JSON**
   - Confirm the relay is valid JSON.
   - Confirm required fields exist: `relay_id`, `from`, `to`, `task`, `message`, `timestamp`, `status`.

4. **Route by Recipient**
   - If `to` is `00`, route to Agent A inbox.
   - If `to` is `01`, route to Agent B inbox.
   - If `to` is unknown, route to dead-letter.

5. **Write Inbox File**
   - Create `relay/inbox/{relay_id}.json`.

6. **Update Recipient Index**
   - Open `relay/index/{to}.json`.
   - Add `{relay_id}.json` to `pending` if it is not already present.
   - Save the index back to GitHub.

7. **Dead Letter Path**
   - If the recipient is invalid or required fields are missing, write a record to `relay/dead-letter/`.

## Minimal n8n Router Logic

The workflow logic is basically:

```text
new file appears in relay/outbox/
        ↓
read file
        ↓
parse JSON
        ↓
if to is valid:
    write relay/inbox/{relay_id}.json
    update relay/index/{to}.json
else:
    write relay/dead-letter/{relay_id or timestamp}.json
```

## Two-Agent Test

### Step 1 — Agent A Creates a Relay

Create:

```text
relay/outbox/000120261380001.json
```

Content:

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

### Step 2 — Let n8n Route It

n8n should create or update:

```text
relay/inbox/000120261380001.json
relay/index/01.json
```

The index should contain:

```json
{
  "agent": "01",
  "pending": [
    "000120261380001.json"
  ],
  "updated": "2026-05-18T12:00:00Z"
}
```

### Step 3 — Agent B Reads It

Ask Agent B to read:

```text
relay/index/01.json
```

Then have Agent B read the listed inbox file.

### Step 4 — Agent B Responds

Agent B creates:

```text
relay/outbox/010020261380002.json
```

Content:

```json
{
  "relay_id": "010020261380002",
  "type": "relay",
  "from": "01",
  "to": "00",
  "task": "Smoke test response",
  "message": "Receipt confirmed.",
  "context": null,
  "history": "000120261380001.json",
  "timestamp": "2026-05-18T12:05:00Z",
  "status": "pending"
}
```

### Step 5 — Let n8n Route the Response Back

n8n should create or update:

```text
relay/inbox/010020261380002.json
relay/index/00.json
```

`relay/index/00.json` should contain:

```json
{
  "agent": "00",
  "pending": [
    "010020261380002.json"
  ],
  "updated": "2026-05-18T12:05:00Z"
}
```

Now Agent A can read the response.

## Manual Testing Without n8n

Manual testing is still useful for learning the structure.

Without n8n, you can simulate routing by copying the relay file from `relay/outbox/` to `relay/inbox/`, then editing the recipient index by hand.

That proves the relay format works, but it is not the recommended long-term workflow.

## Cleanup

Early cleanup should only remove filenames from index `pending` lists.

Do not delete relay records unless you are sure you no longer need the audit trail.

Example before:

```json
{
  "agent": "01",
  "pending": [
    "000120261380001.json"
  ],
  "updated": "2026-05-18T12:00:00Z"
}
```

Example after:

```json
{
  "agent": "01",
  "pending": [],
  "updated": "2026-05-18T12:10:00Z"
}
```

## Privacy Notes

If the repo is public, anyone may be able to see:

- relay messages;
- task names;
- timestamps;
- agent names;
- file history;
- mistakes and test artifacts.

For real work, use a private repository.

For a public demo, use generic examples only.

## Additional Possibilities

This pattern can be expanded later with:

- more agents;
- read/unread states;
- front-end inbox views;
- validation agents;
- task IDs;
- audit logs;
- human approval gates;
- local-only routing;
- GitHub Actions;
- richer n8n workflows;
- multiple model providers;
- archive workflows.

The minimal idea remains:

```text
structured JSON relays + shared GitHub mailbox + n8n routing + predictable index files
```

## License

MIT License.
