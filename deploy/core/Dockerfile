FROM users-base

ENV WEB_SERVER_ADDRESS 0.0.0.0:8000

COPY config.yaml /var/nameko/config.yaml

CMD . /appenv/bin/activate; \
    nameko run --config config.yaml --backdoor-port 3000 users.services.core.service:UsersService