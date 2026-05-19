# RI-Git-Synched-Relays

**R**outing **I**nfrastructure for **Git-Synchronized Relays**

## Foreword

I know very little coding, by way of trying to make a game and getting tired of copy and pasting relays between numerous agents I decided to see what there was for a work around. Maybe there was one already and I didn't know what to look it up as, but as far as I could tell this didn't exist already, or nobody thought to use it this way. I used ChatGPT and Claude alternatively to build it. This was my work around, I didn't code it, I directed its building. So there very likely are tweaks that can improve it. I hope this helps someone create something amazing, or something that makes them feel amazing for having accomplished something. Everything that follows was CGPT written.

— WA-Ladd

## Project Summary

RI-Git-Synched-Relays is a file-based relay pattern for passing structured messages between LLM agents through GitHub, with n8n handling routing.

The core system uses:

- GitHub as a shared relay mailbox;
- JSON relay files as the message format;
- n8n as the router;
- per-agent inbox index files;
- dead-letter handling for invalid relays.

The relay format is model-agnostic. Any LLM agent that can read and write files in the same GitHub repository through a GitHub connector or another read/write bridge can participate.

## Requirements

To deploy the basic two-agent version, you need:

- a GitHub account;
- this repository, forked or copied;
- n8n installed or hosted;
- a GitHub Personal Access Token with repo contents read/write access;
- two LLM agents/chats with access to the GitHub repository through a GitHub connector or another read/write bridge.

If an LLM cannot read and write GitHub files, it cannot participate directly in this relay.

## Quick Start

For the step-by-step setup walkthrough, start here:

```text
docs/QUICK_START.md
```

That guide walks through the smallest working two-agent setup.

## Documentation

| Document | Purpose |
|---|---|
| `docs/QUICK_START.md` | Step-by-step deployment walkthrough |
| `docs/AGENT_PROMPTS.md` | Copy-ready prompts for Agent A and Agent B |
| `docs/FRAMEWORK_GUIDE.md` | Technical explanation of the relay framework |
| `n8n/basic-relay-router-workflow.json` | Importable starter n8n router workflow |
| `examples/relay-example.json` | Example relay file |

## Repository Structure

```text
RI-Git-Synched-Relays/
├── README.md
├── docs/
│   ├── QUICK_START.md
│   ├── AGENT_PROMPTS.md
│   └── FRAMEWORK_GUIDE.md
├── examples/
│   └── relay-example.json
├── n8n/
│   └── basic-relay-router-workflow.json
└── relay/
    ├── outbox/
    ├── inbox/
    ├── index/
    │   ├── 00.json
    │   └── 01.json
    └── dead-letter/
```

## Basic Flow

```text
Agent A writes relay/outbox/*.json
        ↓
n8n reads and validates the relay
        ↓
n8n writes relay/inbox/*.json
        ↓
n8n updates relay/index/{recipient}.json
        ↓
Recipient agent reads its index and inbox
        ↓
Recipient writes a response to relay/outbox/
        ↓
n8n routes the response back
```

## Relay Format

A relay is a JSON file:

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

## Current Starter Agents

```text
00 = Agent A
01 = Agent B
```

Each sender maintains its own relay sequence counter. Counters are per sender, not global.

## Status

Current scope:

- two-agent relay starter;
- GitHub-backed relay mailbox;
- n8n starter router workflow;
- per-agent pending indexes;
- dead-letter path;
- beginner setup guide;
- framework guide for extension.

## Privacy Warning

If this repository is public, relay files may expose:

- messages;
- task names;
- timestamps;
- agent identifiers;
- file history;
- setup mistakes.

Use a private repository for sensitive work.

Do not commit API keys, tokens, private logs, or personal data.

## License

MIT License.
