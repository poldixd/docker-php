import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    'select_builds',
    Path(__file__).resolve().parents[1] / '.github/scripts/select_builds.py',
)
selection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(selection)
VERSIONS = ['8.2', '8.3', '8.4', '8.5']


class BuildSelectionTest(unittest.TestCase):
    def test_documentation_and_dependabot_only_skip_builds(self):
        self.assertEqual(selection.select_versions(
            ['README.md', '.github/dependabot.yml', 'LICENSE'], VERSIONS,
        ), [])

    def test_one_version_builds_only_that_version(self):
        self.assertEqual(selection.select_versions(
            ['php/8.4/Dockerfile', 'README.md'], VERSIONS,
        ), ['8.4'])

    def test_multiple_versions_are_deduplicated(self):
        self.assertEqual(selection.select_versions(
            ['php/8.5/Dockerfile', 'php/8.2/Dockerfile', 'php/8.5/config.ini'], VERSIONS,
        ), ['8.2', '8.5'])

    def test_shared_inputs_build_every_version(self):
        for path in ['php/common/install.sh', 'php/common/imagemagick-policy.xml',
                     'tests/smoke.sh', 'php/common/template.md', '.github/workflows/main.yml',
                     '.github/scripts/select_builds.py', '.dockerignore', 'unknown-file']:
            with self.subTest(path=path):
                self.assertEqual(selection.select_versions([path], VERSIONS), VERSIONS)

    def test_non_pr_events_build_every_version(self):
        for event in ['push', 'schedule', 'workflow_dispatch']:
            with self.subTest(event=event):
                self.assertIsNone(selection.changed_files(event, {}))

    def test_pr_diff_handles_renames_and_an_advanced_base(self):
        # Renames must include both paths; unrelated base changes must be excluded.
        with tempfile.TemporaryDirectory() as directory:
            def git(*args):
                return subprocess.check_output(['git', '-C', directory, *args])

            git('init', '-q')
            old = Path(directory) / 'php/8.3/Dockerfile'
            old.parent.mkdir(parents=True)
            old.write_text('FROM php:8.3-cli\n')
            git('add', '.')
            git('-c', 'user.name=Test', '-c', 'user.email=test@example.com',
                'commit', '-qm', 'initial')
            before = git('rev-parse', 'HEAD').decode().strip()
            new = Path(directory) / 'php/8.4/Dockerfile'
            new.parent.mkdir(parents=True)
            old.rename(new)
            git('add', '-A')
            git('-c', 'user.name=Test', '-c', 'user.email=test@example.com',
                'commit', '-qm', 'rename')
            after = git('rev-parse', 'HEAD').decode().strip()
            git('checkout', '-q', before)
            base_file = Path(directory) / 'php/8.5/Dockerfile'
            base_file.parent.mkdir(parents=True)
            base_file.write_text('FROM php:8.5-cli\n')
            git('add', '.')
            git('-c', 'user.name=Test', '-c', 'user.email=test@example.com',
                'commit', '-qm', 'advance base independently')
            base = git('rev-parse', 'HEAD').decode().strip()
            original = subprocess.check_output
            with patch.object(selection.subprocess, 'check_output',
                              side_effect=lambda args: original(args, cwd=directory)):
                paths = selection.changed_files('pull_request', {
                    'pull_request': {'base': {'sha': base}, 'head': {'sha': after}},
                })
            self.assertEqual(selection.select_versions(paths, VERSIONS), ['8.3', '8.4'])

    def test_github_outputs_for_skipped_and_complete_builds(self):
        for paths, expected_versions in [([], []), (None, VERSIONS)]:
            with self.subTest(paths=paths), tempfile.TemporaryDirectory() as directory:
                event_file = Path(directory) / 'event.json'
                output_file = Path(directory) / 'output'
                event_file.write_text('{}')
                environment = {
                    'GITHUB_EVENT_PATH': str(event_file),
                    'GITHUB_EVENT_NAME': 'workflow_dispatch',
                    'GITHUB_OUTPUT': str(output_file),
                }
                with patch.dict(os.environ, environment), \
                     patch.object(selection, 'changed_files', return_value=paths), \
                     patch('builtins.print'):
                    selection.main()
                outputs = dict(line.split('=', 1) for line in output_file.read_text().splitlines())
                self.assertEqual(json.loads(outputs['matrix']), {
                    'version': expected_versions, 'variant': ['base', 'chromium'],
                })
                self.assertEqual(outputs['has_changes'], 'true' if expected_versions else 'false')


if __name__ == '__main__':
    unittest.main()
