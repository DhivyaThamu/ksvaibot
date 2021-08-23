FROM rasa/rasa:2.8.1

COPY app /app
COPY server.sh /app/server.sh
COPY requirements.txt /app/requirements.txt

USER root
RUN pip install --upgrade pip

RUN rasa train
RUN pip install --requirement /app/requirements.txt
RUN rasa run actions
RUN chmod a+rwx /app/server.sh

ENTRYPOINT ["/app/server.sh"]
