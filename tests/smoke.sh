#!/bin/sh
set -eu

php /tmp/image-tests/runtime.php
XDEBUG_MODE=coverage php /tmp/image-tests/coverage.php
composer --version
node --version
npm --version
yarn --version

if [ "${1:-false}" = true ]; then
    browser_tmp=$(mktemp -d)
    trap 'rm -rf "$browser_tmp"' EXIT HUP INT TERM
    timeout 45s chromium --headless --no-sandbox --disable-dev-shm-usage \
        --user-data-dir="$browser_tmp/profile" --dump-dom \
        'data:text/html,<html><body><script>document.body.textContent="browser-ok"</script></body></html>' \
        > "$browser_tmp/result.html"
    grep -q '<body>browser-ok</body>' "$browser_tmp/result.html"
else
    if command -v chromium >/dev/null 2>&1; then
        echo 'Base image unexpectedly contains Chromium' >&2
        exit 1
    fi
fi
