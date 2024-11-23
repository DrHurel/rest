FROM postgres:17

ARG DATA_FILE
ARG SERVICE_SCHEMA
ARG EXPOSED_PORT

COPY  databases/${SERVICE_SCHEMA}/*.sql /docker-entrypoint-initdb.d/
COPY databases/${SERVICE_SCHEMA}/${DATA_FILE}/*.sql /docker-entrypoint-initdb.d/

RUN chmod a+r /docker-entrypoint-initdb.d/*
EXPOSE ${EXPOSED_PORT}