FROM node
RUN apt-get update || : && apt-get install python3 -y && \
npm install -g solc && npm install -g npm@9.6.7

RUN apt-get install python3-pip -y && npm install @openzeppelin/contracts

COPY . .

RUN pip3 install slither-analyzer && pip3 install -r requirements.txt


CMD python3 ./app/__init__.py
