FROM rasa/rasa:2.8.1

COPY app /app
COPY server.sh /app/server.sh

USER root

RUN rasa train
RUN chmod a+rwx /app/server.sh

ENTRYPOINT ["/app/server.sh"]
RUN chmod a+rwx /app/action.sh

ENTRYPOINT ["/app/action.sh"] 
