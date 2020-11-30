FROM python:3.8-alpine3.10


RUN echo "http://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories


RUN apk update

RUN apk --no-cache --update-cache add gcc gfortran build-base wget freetype-dev libpng-dev openblas-dev postgresql-dev
RUN pip install -U pip


RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
EXPOSE 5000
ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0" ]


