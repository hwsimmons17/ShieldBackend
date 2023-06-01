FROM node
RUN apt-get update || : && apt-get install python3 -y && \
npm install -g solc

RUN apt-get install python3-pip -y

COPY . .

RUN pip3 install slither-analyzer && pip3 install -r requirements.txt


CMD python3 ./app/__init__.py
