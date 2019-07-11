FROM service-builder AS wheels

COPY . /application

RUN cd /application && pip wheel .

# ----------------------------------

FROM service-base AS install

COPY --from=wheels /application/wheelhouse /wheelhouse

RUN pip install --no-index -f /wheelhouse users

# ----------------------------------

FROM service-base AS service

COPY --from=install /appenv /appenv

COPY config.yaml /var/nameko/config.yaml

USER nameko

WORKDIR /var/nameko

EXPOSE 8000

CMD . /appenv/bin/activate && \
    nameko run --config config.yaml users.services.core.service:UsersService --backdoor 3000