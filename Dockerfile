
FROM python-base:latest as base

ADD wheelhouse /application/wheelhouse

WORKDIR /application

RUN . /appenv/bin/activate; \
    pip install --no-index -f wheelhouse users

# -----

FROM python-base:latest 

COPY --from=base /appenv /appenv

WORKDIR /var/nameko

EXPOSE 8000