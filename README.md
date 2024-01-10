# Docker PHP Image

It's my personal Docker PHP Image for the CI. Everything you need to test a Laravel application is on board. You can find the image on the docker hub: https://hub.docker.com/repository/docker/poldixd/php/general

## Build locally

```bash
$ docker build . -t php-docker -f php/8.3/Dockerfile
```

## Use it in your .gitlab-ci.yml

```yml
test:
  stage: test
  image: poldixd/php:8.3
  script:
    - php vendor/bin/pest --coverage
```

## Contributing

Feel free to create a pull request.

## Credits

- Special thanks to [edbizarro](https://github.com/edbizarro)