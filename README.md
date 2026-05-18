# RI-Git-Synched-Relays

**R**outing **I**nfrastructure for **Git-Synchronized Relays**

## Foreword

I know very little coding, by way of trying to make a game and getting tired of copy and paste I decided to see what there was for a work around. Maybe there was one and I didn't know what to look it up as, but as far as I could tell this didn't exist already, or nobody thought to use it this way. I used ChatGPT and Claude alternatively to build it. My setup also has API agents who are called on for tasks like code and logic verification. This was my work around, I didn't code it, I directed its building. So there very likely are tweaks that can improve it. I hope this helps someone create something amazing, or something that makes them feel amazing for having accomplished something.

— WA-Ladd

## Overview

This project describes a simple relay pattern for passing structured messages between LLM agents using GitHub as a shared mailbox.

The core idea is:

- A message is written as a JSON file.
- The JSON file has a known sender, recipient, task, and message.
- A receiving agent can read the file through a GitHub connector.
- A response can be written back as another JSON relay.
- Optional automation can move messages between outbox, inbox, index, and dead-letter folders.

The relay format is the important part. The specific model provider is not.

Any LLM that can read and write files in the same GitHub repository can participate.

## What This Is

This is a minimal communication layer for LLM-assisted workflows.

It is useful when:

- you want two AI agents to pass tasks between each other;
- you do not want to manually copy and paste every relay;
- you want a visible record of what was sent;
- you want a simple Git-based structure instead of a full orchestration platform.

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
Router or human moves/copies it to relay/inbox/
        ↓
relay/index/01.json is updated
        ↓
Agent B reads relay/index/01.json
        ↓
Agent B opens the listed relay file
        ↓
Agent B writes a response relay back to Agent A
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

### Step 2 — Route It Manually

Copy the file into:

```text
relay/inbox/000120261380001.json
```

Then update:

```text
relay/index/01.json
```

to:

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

### Step 5 — Route the Response Back

Copy it to:

```text
relay/inbox/010020261380002.json
```

Update:

```text
relay/index/00.json
```

to:

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

## Optional Router Automation

After the manual test works, the routing step can be automated.

A simple router can:

1. Watch for new files in `relay/outbox/`
2. Read the JSON
3. Check the `to` field
4. Copy the relay to `relay/inbox/`
5. Update `relay/index/{to}.json`
6. Send invalid relays to `relay/dead-letter/`

This can be done with:

- n8n
- GitHub Actions
- a local Python script
- a small web server
- another automation tool

## Minimal Router Pseudocode

```text
for each new relay in relay/outbox:
    read JSON

    if relay.to is not a known recipient:
        write/copy relay to relay/dead-letter
        stop

    write/copy relay to relay/inbox/{relay_id}.json

    open relay/index/{to}.json
    append {relay_id}.json to pending
    save relay/index/{to}.json
```

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
- n8n workflows;
- multiple model providers;
- archive workflows.

The minimal idea remains:

```text
structured JSON relays + shared GitHub mailbox + predictable index files
```

## License

MIT License.
