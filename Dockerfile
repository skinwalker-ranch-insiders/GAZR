FROM python:3.9-alpine
WORKDIR /usr/src/gazr
COPY requirements.txt .
RUN apk update && apk add tzdata unixodbc-dev gcc g++ 
RUN pip install -r requirements.txt
ENV TZ="America/Boise"
CMD [ "sh", "./rcloak.sh" ]
