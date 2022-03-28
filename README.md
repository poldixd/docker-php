# Docker PHP Image

It's my personal Docker PHP Image for the CI. Everything you need to test a Laravel application is on board. There are some versions:

| Tag             | PHP Version |
| --------------- | ----------- |
| poldixd/php:8.0 | PHP 8.0     |
| poldixd/php:8.1 | PHP 8.1     |

## Build locally

```bash
$ docker build . -t php-docker -f php/8.1/Dockerfile
```

## Use it in your .gitlab-ci.yml

```yml
test:
  stage: test
  image: poldixd/php:8.1
  script:
    - php vendor/bin/pest --coverage
```

## Contributing

Feel free to create a pull request.

## Credits

- Special thanks to [edbizarro](https://github.com/edbizarro)