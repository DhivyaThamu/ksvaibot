FROM rasa/rasa:2.8.1

COPY app /app
COPY server.sh /app/server.sh

USER root

RUN rasa train
RUN chmod a+rwx /app/server.sh
CMD [ "rasa","run","actions","--port","5055"]

ENTRYPOINT ["/app/server.sh"]
