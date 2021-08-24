FROM rasa/rasa:2.8.1

COPY app /app
COPY server.sh /app/server.sh
COPY requirements.txt /app/requirements.txt


USER root
RUN apt-get update
RUN apt-get -y install libasound-dev portaudio19-dev libportaudio2
RUN python3.8 -m pip install sounddevice==0.4.2

RUN rasa train
RUN rasa run actions

RUN chmod a+rwx /app/server.sh

ENTRYPOINT ["/app/server.sh"]
