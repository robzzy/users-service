FROM users-base

COPY alembic /var/nameko/alembic

COPY alembic.ini /var/nameko/alembic.ini

CMD . /appenv/bin/activate && \
    alembic upgrade $REVISION || alembic downgrade $REVISION
