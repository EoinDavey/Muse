from node:10-alpine

RUN npm i -g @angular/cli

RUN apk add python3 \
    py3-pip \
    ffmpeg

RUN pip3 install --upgrade pip &&\
    pip3 install textx &&\
    pip3 install pydub &&\
    pip3 install flask &&\
    pip3 install flask-cors

WORKDIR /srv/muse

EXPOSE 4200
EXPOSE 5000

ENV FLASK_APP server.py

COPY . .

CMD ["./run.sh"]
