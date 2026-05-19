# Framework Guide

This document explains the relay framework itself.

Read this if you want to:

- modify the routing system;
- add more agents;
- extend the relay format;
- build automation around the relay structure;
- experiment with memory-style retrieval;
- integrate other orchestration systems.

## Core Concept

The framework treats GitHub as a shared structured mailbox.

Agents communicate by writing JSON relay files.

n8n handles routing.

The relay framework intentionally separates:

- relay creation;
- relay routing;
- inbox indexing;
- dead-letter handling;
- cleanup.

## Relay Flow

```text
Agent writes relay → relay/outbox/
        ↓
n8n reads relay
        ↓
n8n validates relay
        ↓
if valid:
    route to relay/inbox/
    update relay/index/{recipient}.json
else:
    route to relay/dead-letter/
```

## Why GitHub

GitHub provides:

- version history;
- structured storage;
- easy API access;
- connector support in multiple LLM systems;
- visible audit trails;
- simple file-based interoperability.

The relay format itself is not tied to GitHub specifically, but GitHub is currently the easiest common bridge.

## Relay Structure

Example:

```json
{
  "relay_id": "000120261380001",
  "type": "relay",
  "from": "00",
  "to": "01",
  "task": "Review this plan",
  "message": "Please review this plan for gaps or risks.",
  "context": null,
  "history": null,
  "timestamp": "2026-05-18T12:00:00Z",
  "status": "pending"
}
```

## Relay Fields

| Field | Purpose |
|---|---|
| relay_id | Unique relay identifier |
| type | Relay type |
| from | Sender ID |
| to | Recipient ID |
| task | Short request summary |
| message | Main relay content |
| context | Optional external reference |
| history | Optional previous relay reference |
| timestamp | ISO 8601 timestamp |
| status | Relay state |

## Relay IDs

Current format:

```text
{from}{to}{year}{julian_day}{sequence}
```

Example:

```text
000120261380001
```

Meaning:

```text
00    sender
01    recipient
2026  year
138   julian day
0001  sender sequence counter
```

Counters are sender-specific, not global.

## Index Files

Each recipient has an inbox index:

```text
relay/index/00.json
relay/index/01.json
```

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

The index exists so agents do not need to scan the entire inbox folder.

## Dead Letter

Invalid relays are written into:

```text
relay/dead-letter/
```

Examples:

- invalid recipient;
- malformed JSON;
- missing required fields.

Dead-letter handling is intentionally separate from inbox routing.

## Cleanup

Cleanup should only remove handled filenames from index pending lists.

Relay records themselves should usually remain intact during testing.

Example:

Before:

```json
{
  "agent": "01",
  "pending": [
    "000120261380001.json"
  ]
}
```

After:

```json
{
  "agent": "01",
  "pending": []
}
```

## Adding More Agents

To add a new agent:

1. Assign a new ID.
2. Create a new index file.
3. Update routing validation.
4. Give the agent its own prompt.

Example:

```text
02 = Agent C
03 = Agent D
```

New indexes:

```text
relay/index/02.json
relay/index/03.json
```

The router must treat those IDs as valid recipients.

## Memory-Style Extensions

The relay structure can support memory-style retrieval later.

Because relay records are structured and timestamped, they can potentially become searchable project memory.

That requires additional logic for:

- retrieval;
- filtering;
- cleanup;
- trust boundaries;
- archival rules;
- privacy controls.

The relay framework itself should remain separate from memory policy.

## Design Goals

The current framework emphasizes:

- simplicity;
- visibility;
- inspectable routing;
- append-style records;
- interoperability;
- easy debugging;
- minimal assumptions.

The goal is not to hide routing logic.

The goal is to make routing visible and understandable.
