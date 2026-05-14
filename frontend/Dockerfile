# Этап 1 — сборка React
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Этап 2 — nginx раздаёт готовые файлы
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html