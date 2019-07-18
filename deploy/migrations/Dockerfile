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

COPY alembic /var/nameko/alembic

COPY alembic.ini /var/nameko/alembic.ini

USER nameko

WORKDIR /var/nameko

CMD . /appenv/bin/activate && \
    alembic upgrade $REVISION || alembic downgrade $REVISION