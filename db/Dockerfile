FROM mysql/mysql-server:8.0.23

ADD init-db.sh /docker-entrypoint-initdb.d/

ADD schema.sql fake-data.sql /tmp/

WORKDIR /tmp

RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

EXPOSE 3306
