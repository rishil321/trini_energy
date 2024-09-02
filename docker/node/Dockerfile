FROM node:20-alpine

ENV NODE_ENV=production

WORKDIR /code

COPY ./react_frontend/package.json ./react_frontend/package-lock.json /code/

RUN npm install --production --no-progress

COPY . .

CMD [ "npm", "start" ]