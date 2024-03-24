#Frontend service
FROM nginx:stable-alpine3.17-slim AS frontendamqp
ARG MY_VARIABLE
ENV MY_VARIABLE=$MY_VARIABLE
ADD ./amqp /usr/share/nginx/html
EXPOSE 80

#Frontend service
FROM nginx:stable-alpine3.17-slim AS frontendapi
ARG MY_VARIABLE
ENV MY_VARIABLE=$MY_VARIABLE
ADD ./api /usr/share/nginx/html
EXPOSE 81

#Frontend Wrapper
FROM python:3.9.19-alpine3.19 AS wrapper
ADD . /app
EXPOSE 8080
WORKDIR /app
RUN pip install pika
CMD ["python", "fwrapper.py"]
