import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / 'setup'
CONFIG_PATH = CONFIG_DIR / 'config.json'

WEBHOOK_TEMPLATE = ROOT / 'n8n' / 'basic-relay-router-webhook.json'
WEBHOOK_OUTPUT = ROOT / 'n8n' / 'basic-relay-router-webhook.configured.json'

MANUAL_TEMPLATE = ROOT / 'n8n' / 'basic-relay-router-workflow.json'
MANUAL_OUTPUT = ROOT / 'n8n' / 'basic-relay-router-workflow.configured.json'


def ask(prompt, default=None):
    if default:
        value = input(f'{prompt} [{default}]: ').strip()
        return value or default
    while True:
        value = input(f'{prompt}: ').strip()
        if value:
            return value
        print('Please enter a value.')


def yes_no(prompt, default=True):
    suffix = 'Y/n' if default else 'y/N'
    value = input(f'{prompt} [{suffix}]: ').strip().lower()
    if not value:
        return default
    return value in ('y', 'yes')


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        f.write('\n')


def configure_workflow(template_path, output_path, owner, repo, branch):
    workflow = load_json(template_path)

    for node in workflow.get('nodes', []):
        params = node.get('parameters', {})
        code = params.get('jsCode')
        if isinstance(code, str):
            code = code.replace("const owner = 'YOUR_GITHUB_USERNAME';", f"const owner = '{owner}';")
            code = code.replace("const repo = 'RI-Git-Synched-Relays';", f"const repo = '{repo}';")
            code = code.replace("const branch = 'main';", f"const branch = '{branch}';")
            params['jsCode'] = code

    save_json(output_path, workflow)


def write_index(agent_id):
    path = ROOT / 'relay' / 'index' / f'{agent_id}.json'
    data = {
        'agent': agent_id,
        'pending': [],
        'updated': None
    }
    save_json(path, data)


def touch(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)


def main():
    print('\nRI-Git-Synched-Relays Setup Wizard')
    print('This prepares a two-agent relay setup.\n')
    print('This wizard does not ask for your GitHub PAT.')
    print('Store your PAT only inside n8n credentials.\n')

    owner = ask('GitHub username or organization')
    repo = ask('Repository name', 'RI-Git-Synched-Relays')
    branch = ask('Branch', 'main')

    make_manual = yes_no('Also create manual fallback workflow', True)

    config = {
        'github_owner': owner,
        'github_repo': repo,
        'branch': branch,
        'agent_ids': ['00', '01'],
        'webhook_workflow_output': str(WEBHOOK_OUTPUT.relative_to(ROOT)),
        'manual_workflow_output': str(MANUAL_OUTPUT.relative_to(ROOT)) if make_manual else None
    }
    save_json(CONFIG_PATH, config)

    configure_workflow(WEBHOOK_TEMPLATE, WEBHOOK_OUTPUT, owner, repo, branch)
    if make_manual:
        configure_workflow(MANUAL_TEMPLATE, MANUAL_OUTPUT, owner, repo, branch)

    write_index('00')
    write_index('01')

    touch(ROOT / 'relay' / 'outbox' / '.gitkeep')
    touch(ROOT / 'relay' / 'inbox' / '.gitkeep')
    touch(ROOT / 'relay' / 'dead-letter' / '.gitkeep')

    print('\nDone. Created/updated:')
    print(f'- {WEBHOOK_OUTPUT.relative_to(ROOT)}')
    if make_manual:
        print(f'- {MANUAL_OUTPUT.relative_to(ROOT)}')
    print('- relay/index/00.json')
    print('- relay/index/01.json')
    print('- relay/outbox/.gitkeep')
    print('- relay/inbox/.gitkeep')
    print('- relay/dead-letter/.gitkeep')
    print('- setup/config.json')

    print('\nNext steps:')
    print('1. Import n8n/basic-relay-router-webhook.configured.json into n8n.')
    print('2. In n8n, create an HTTP Header Auth credential:')
    print('   Header Name: Authorization')
    print('   Header Value: Bearer YOUR_GITHUB_PAT')
    print('3. Attach that credential to the GitHub request nodes.')
    print('4. Activate the workflow and copy the production webhook URL.')
    print('5. In GitHub: Settings -> Webhooks -> Add webhook.')
    print('6. Paste the n8n webhook URL. Use content type application/json and push events only.')
    print('7. Give Agent A and Agent B the prompts in docs/AGENT_PROMPTS.md.')
    print('8. Create the smoke-test relay from examples/relay-example.json.\n')


if __name__ == '__main__':
    main()
