FROM rasa/rasa:2.8.1

COPY app /app
COPY app /app/actions
COPY server.sh /app/server.sh
COPY requirements.txt /app/requirements.txt


USER root

RUN pip install sounddevice
RUN rasa train

RUN chmod a+rwx /app/server.sh

ENTRYPOINT ["/app/server.sh"]
