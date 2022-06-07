FROM node:16
WORKDIR /home/node/app

COPY package*  /home/node/app
RUN npm ci

# replace this with your application's default port
EXPOSE 3000

