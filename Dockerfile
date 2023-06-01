FROM node
RUN apt-get update || : && apt-get install python3 -y && \
npm install -g solc

RUN apt-get install python3-pip -y

WORKDIR /usr/app
COPY . .

RUN pip3 install slither-analyzer && pip3 install -r requirements.txt


RUN npm install @openzeppelin/contracts


CMD python3 ./app/__init__.py
