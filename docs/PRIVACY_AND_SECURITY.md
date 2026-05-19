# Privacy and Security

This project is designed as a local setup helper and GitHub/n8n relay pattern.

It does not include a hosted service controlled by this project.

It does not collect analytics.

It does not send setup data to the project author.

It does not store your GitHub Personal Access Token in this repository.

## What Data Exists

The relay system uses files in your GitHub repository.

That means your data is wherever you choose to put the repo:

- your GitHub account;
- your n8n instance;
- your local computer, if you clone the repo;
- any LLM agent or connector you choose to give access to the repo.

You control the repository and the services you connect to it.

## What the Setup Helper Does

The local setup helper reads local configuration values such as:

- GitHub username;
- repository name;
- branch name;
- agent IDs.

It uses those values to generate configured local files, such as an n8n workflow JSON file.

It does not need your GitHub PAT.

It does not upload your PAT.

It does not transmit setup answers to the project author.

It does not create a database.

It does not create persistent memory.

## GitHub Token Handling

Your GitHub PAT should be stored in n8n as a credential.

Do not paste your PAT into:

- README files;
- relay files;
- setup config files;
- screenshots;
- public issues;
- public commits.

GitHub says to treat access tokens like passwords and recommends using fine-grained personal access tokens when possible. GitHub also explains that fine-grained tokens can be limited to specific repositories and permissions.

Official GitHub documentation:

- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

## n8n Credential Handling

The n8n workflow expects your GitHub PAT to be stored as an n8n credential.

The workflow files in this repo use placeholder credential names and IDs.

You must replace those placeholders inside your own n8n instance.

Official n8n credential documentation:

- https://docs.n8n.io/credentials/

## GitHub Webhook Handling

The webhook connects your GitHub repository to your n8n workflow.

When a push happens, GitHub sends a webhook event to your n8n webhook URL.

This project only uses the webhook to notice new relay files in `relay/outbox/`.

Official GitHub webhook documentation:

- https://docs.github.com/en/webhooks

## Public Repo Warning

If your relay repository is public, other people may be able to see:

- relay messages;
- task names;
- timestamps;
- agent IDs;
- setup mistakes;
- commit history.

Use a private repo for real work.

Use a public repo only for demos, examples, and non-sensitive testing.

## LLM Connector Warning

Each LLM agent or chat connector has its own privacy and data handling policies.

This project cannot control how third-party LLM providers handle data.

Before using private information, check the privacy settings and data policy of the tools you connect.

## No Warranty

This project is provided as a starter kit.

You are responsible for:

- where you deploy it;
- what data you put in relay files;
- which services you connect;
- which agents you give access to;
- which tokens and permissions you grant.

## Recommended Safe Defaults

For first setup:

- use a private GitHub repo;
- use a fine-grained GitHub PAT;
- limit the PAT to this repo only;
- give the PAT only the permissions required to read and write repository contents;
- store the PAT only inside n8n credentials;
- do not add private logs or secrets to relay messages;
- test with dummy messages first.
