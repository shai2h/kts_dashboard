FROM node:20-alpine

WORKDIR /app/dashboard

COPY dashboard/package*.json ./
RUN npm install

COPY . .

RUN npm run build

CMD ["npm", "run", "start"]
