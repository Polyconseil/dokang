FROM alpine
MAINTAINER Polyconseil <opensource+dokang@polyconseil.fr>

VOLUME ['/home/dokang/data']
EXPOSE 6543

RUN adduser -u 998 -D dokang
COPY ./files /home/dokang/
RUN chown -R dokang:dokang /home/dokang

RUN apk add --no-cache --update python3

USER dokang
WORKDIR /home/dokang

RUN python3 -m venv venv && \
    venv/bin/pip install dokang dokang_pdf waitress

ENTRYPOINT ["/home/dokang/venv/bin/python3", "entrypoint.py"]
