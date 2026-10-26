# Docker PHP Image

Personal PHP CLI images for testing Laravel applications in CI, published as
[`poldixd/php`](https://hub.docker.com/r/poldixd/php).

Supported tags: `8.2`, `8.3`, `8.4`, `8.5`, plus a `-chromium` variant of each.
All are built for `linux/amd64` and `linux/arm64` on Debian Trixie.

## Included tools

- Composer, Node.js 24 (including its bundled npm), Corepack and Yarn.
- MySQL/MariaDB client, Git, SSH client and rsync.
- PHP extensions for MySQL, PostgreSQL, SQLite, Redis, MongoDB, image processing,
  and Xdebug coverage. See `php/common/install.sh` for the shared installation.
- ImageMagick and Ghostscript, with PDF conversion explicitly allowed.
- Chromium and Playwright system dependencies **only** in `-chromium` images.
  Playwright browsers and the project's Playwright package are not preinstalled.

Xdebug coverage is enabled by default, so `pest --coverage` works without extra
configuration. Set `XDEBUG_MODE=off` in jobs that do not need coverage to avoid
its overhead. PCOV is not installed.
PHPCS is no longer installed globally: declare lint tools in your application's
`composer.json` and use the versions recorded in its `composer.lock`.

## Build locally

Run from the repository root. The existing Dockerfile paths are unchanged;
installation logic and the ImageMagick policy are shared in `php/common/`.
The default target also runs the smoke tests.

```bash
docker build --build-arg INSTALL_CHROMIUM=false \
  -t poldixd/php:8.4 -f php/8.4/Dockerfile .

docker build --build-arg INSTALL_CHROMIUM=true \
  -t poldixd/php:8.4-chromium -f php/8.4/Dockerfile .
```

For troubleshooting only, `--target runtime` skips the smoke tests.

## Use in GitLab CI

```yaml
test:
  stage: test
  image: poldixd/php:8.4
  script:
    - composer install --no-interaction --prefer-dist
    - php vendor/bin/pest --coverage
```

For browser tests, use `poldixd/php:8.4-chromium`. Configure your browser tool
explicitly when using system Chromium (`/usr/bin/chromium`). A root-run Chromium
needs `--no-sandbox`; use it for trusted application tests. Playwright projects
that use downloaded browsers should install the browser version matching their
locked Playwright package. System dependencies here are pinned to Playwright
1.64.0 and may need updating when your project upgrades Playwright.

## Builds and maintenance

Pull requests build and test without registry credentials or publishing. They
build only the PHP versions whose directories changed, with both variants on
native AMD64. Main-branch, manual and scheduled builds run AMD64 and ARM64 on
separate native runners, without QEMU. Each PR build job has a 30-minute timeout;
a failed job cancels remaining matrix jobs. PRs changing only `README.md`,
`LICENSE` or `.github/dependabot.yml`
skip image builds. Shared installation, test, workflow or other input changes
rebuild all versions. New commits cancel older runs of the same PR.
The stable `Image checks` job reports success for documentation-only changes too
and can be used as the required branch-protection check.

Main-branch pushes, manual runs and weekly scheduled runs build all versions.
This ensures changes are included even if GitHub replaces a pending main-branch
run. Publishing is restricted to main. All native build jobs must pass before
the publish stage combines their digests into multi-platform image tags.
Tests check required PHP extensions, SQLite,
actual Xdebug coverage collection, PDF-to-PNG
conversion, command-line tools, and Chromium execution where applicable.

BuildKit caches are scoped per PHP version, variant and architecture. Tests run
on every build; PRs export only final-image layers to keep cache uploads small. Main-branch,
manual and scheduled builds also cache intermediate stages. Weekly builds
bypass runtime cache to refresh Debian packages. A failed build prevents tag
publication. Each PHP version/variant has a separate publishing job; publication
failures fail the workflow and can leave some tags updated and others unchanged.

PHP, Composer, Node and the extension-installer image use explicit release tags;
Dependabot checks the Dockerfiles every weekday at 08:00 Europe/Berlin and
GitHub Actions every Monday at the same time. Shared PECL, Corepack, Yarn and
Playwright versions are pinned in `php/common/install.sh` and require deliberate
updates there. Keep all four Dockerfiles' tool image
versions in sync. Debian packages and upstream image tags remain mutable;
these builds are not bit-for-bit reproducible.

## Contributing

Feel free to create a pull request.

## Credits

Special thanks to [edbizarro](https://github.com/edbizarro).
