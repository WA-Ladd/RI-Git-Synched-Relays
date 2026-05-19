import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CONFIG_PATH = ROOT / 'setup' / 'config.json'
EXAMPLE_PATH = ROOT / 'setup' / 'config.example.json'

if not CONFIG_PATH.exists():
    print('\nconfig.json not found.\n')
    print('Copy setup/config.example.json to setup/config.json and edit the values first.\n')
    raise SystemExit(1)

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

workflow_template = ROOT / config['n8n_workflow_template']
workflow_output = ROOT / config['n8n_workflow_output']

with open(workflow_template, 'r', encoding='utf-8') as f:
    workflow = json.load(f)

owner = config['github_owner']
repo = config['github_repo']
branch = config.get('branch', 'main')

for node in workflow.get('nodes', []):
    if node.get('name') == 'Configure Repo':
        code = node['parameters']['jsCode']
        code = code.replace('YOUR_GITHUB_USERNAME', owner)
        code = code.replace('RI-Git-Synched-Relays', repo)
        code = code.replace("const branch = 'main';", f"const branch = '{branch}';")
        node['parameters']['jsCode'] = code

workflow_output.parent.mkdir(parents=True, exist_ok=True)

with open(workflow_output, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2)

print('\nConfigured workflow created:')
print(workflow_output)
print('\nNext step:')
print('Import the configured workflow into n8n.')
