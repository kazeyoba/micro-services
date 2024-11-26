FROM postgres:alpine3.17

COPY docker-entrypoint-initdb.d /docker-entrypoint-initdb.d

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=lannion1234

EXPOSE 5432

CMD ["postgres", "-D", "/var/lib/postgresql/data"]