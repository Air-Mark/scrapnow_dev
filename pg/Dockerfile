FROM postgres:10.3


ADD ./restore_db.sh /docker-entrypoint-initdb.d/restore_db.sh
ADD ./latest.sql /latest.sql
ADD ./postgresql.conf /postgresql.conf
RUN chmod 777 /docker-entrypoint-initdb.d/restore_db.sh

CMD ["postgres"]
