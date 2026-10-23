"""Build changed PHP versions in PRs, and all versions when publishing."""

import json
import os
from pathlib import Path
import subprocess


def select_versions(paths, versions):
    """Return affected versions in their original order."""
    selected = set()
    for path in paths:
        if path in {'README.md', 'LICENSE', '.github/dependabot.yml'}:
            continue
        parts = path.split('/')
        if len(parts) >= 3 and parts[0] == 'php' and parts[1] in versions:
            selected.add(parts[1])
        else:
            # Shared or unknown build inputs can affect every image.
            return list(versions)
    return [version for version in versions if version in selected]


def changed_files(event_name, event):
    """Return PR changes, or None to request a complete build."""
    if event_name != 'pull_request':
        # GitHub may replace pending main-branch runs. A complete build also
        # covers changes from any skipped run, rather than only the last push.
        return None
    pull_request = event['pull_request']
    base = pull_request['base']['sha']
    head = pull_request['head']['sha']
    result = subprocess.check_output(
        ['git', 'diff', '--name-only', '--no-renames', '-z', f'{base}...{head}', '--']
    )
    return [os.fsdecode(path) for path in result.split(b'\0') if path]


def main():
    versions = sorted(path.parent.name for path in Path('php').glob('[0-9]*/Dockerfile'))
    if not versions:
        raise RuntimeError('No supported PHP Dockerfiles found')
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    paths = changed_files(os.environ['GITHUB_EVENT_NAME'], event)
    selected = versions if paths is None else select_versions(paths, versions)
    matrix = {'version': selected, 'variant': ['base', 'chromium']}
    matrix_json = json.dumps(matrix, separators=(',', ':'))
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
        output.write(f'matrix={matrix_json}\n')
        output.write(f'has_changes={str(bool(selected)).lower()}\n')
    print(f'PHP versions to build: {", ".join(selected) or "none"}')


if __name__ == '__main__':
    main()
