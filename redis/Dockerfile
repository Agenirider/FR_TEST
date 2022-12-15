FROM redis

RUN mkdir -p /data/bases
RUN mkdir -p /data/log

RUN chown -R redis:redis /data
RUN chmod -R 775 /data

COPY redis.conf /usr/local/etc/redis/redis.conf

# Define default command.


# Expose ports.
EXPOSE 6379