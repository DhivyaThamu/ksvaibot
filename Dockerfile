FROM rasa/rasa:2.8.1

COPY app /app
COPY voiceBiometric /app/voiceBiometric
COPY mongo /app/mongo
COPY server.sh /app/server.sh

USER root

RUN rasa train
RUN rasa run actions
RUN chmod a+rwx /app/server.sh

ENTRYPOINT ["/app/server.sh"]
