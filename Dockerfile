FROM rasa/rasa:2.8.1

COPY app /app
COPY app /app/actions
COPY server.sh /app/server.sh
COPY requirements.txt /app/requirements.txt


USER root
RUN apt-get update
RUN apt-get install libasound-dev portaudio19-dev libportaudio2


RUN rasa train
RUN rasa run actions

RUN chmod a+rwx /app/server.sh

ENTRYPOINT ["/app/server.sh"]
