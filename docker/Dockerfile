FROM alpine
MAINTAINER Polyconseil <opensource+dokang@polyconseil.fr>

EXPOSE 6543

RUN apk add --no-cache --update python3
RUN adduser -u 998 -D dokang

COPY ./files /home/dokang/
RUN mkdir /home/dokang/data
RUN chown -R dokang:dokang /home/dokang
VOLUME ['/home/dokang/data']

USER dokang
WORKDIR /home/dokang

RUN python3 -m venv venv && \
    venv/bin/pip install dokang dokang_pdf waitress

ENV PYTHONPATH=/home/dokang
ENTRYPOINT ["/home/dokang/venv/bin/python3", "entrypoint.py"]
