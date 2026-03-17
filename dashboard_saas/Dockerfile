# Build stage
FROM node:20-slim AS build
WORKDIR /app
COPY dashboard_saas/package*.json ./
RUN npm install
COPY dashboard_saas/ ./
RUN npm run build

# Production stage
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
