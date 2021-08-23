FROM rasa/rasa:2.8.1

COPY app /app
COPY server.sh /app/server.sh
COPY requirements.txt /app/requirements.txt
COPY actions.py /app/actions/actions.py

USER root
RUN pip install sounddevice --user

RUN rasa train

RUN rasa run actions
RUN chmod a+rwx /app/server.sh

ENTRYPOINT ["/app/server.sh"]
