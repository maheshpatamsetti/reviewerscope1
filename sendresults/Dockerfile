
FROM python:3.8.7-slim-buster

WORKDIR /app

COPY sendresults sendresults/

WORKDIR /app/sendresults

RUN pip install -r requirements.txt

EXPOSE 9095

ENTRYPOINT [ "python" ]

CMD [ "send.py" ]
