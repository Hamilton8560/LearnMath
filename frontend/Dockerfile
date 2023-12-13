FROM node:18-alpine AS build
WORKDIR /app

RUN npm install -g @angular/cli

COPY package*.json ./
RUN npm install
COPY . .
RUN ng build

EXPOSE $PORT

CMD ["ng", "serve", "--host", "0.0.0.0"]

