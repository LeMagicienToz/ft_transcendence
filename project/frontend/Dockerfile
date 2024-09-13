FROM node:18-bullseye

WORKDIR /app

COPY package*.json ./

RUN npm install && \
    npm install react-bootstrap bootstrap && \
    npm install react react-router-dom && \
    npm install framer-motion

COPY . .

CMD ["npm", "run", "dev"]