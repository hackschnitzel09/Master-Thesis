#Backend
FROM python:3.9.19-alpine3.19 AS backend
ADD . /app
WORKDIR /app
RUN pip install flask && pip install flask_cors
EXPOSE 5011
ENV FLASK_APP=endpoint.py
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5011"]

#Backend Wrapper
FROM python:3.9.19-alpine3.19 AS wrapper
ADD . /app
WORKDIR /app
RUN pip install pika && pip install requests
CMD ["python", "bwrapper.py"]
