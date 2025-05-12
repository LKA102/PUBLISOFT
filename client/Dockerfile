# stage1 as builder
FROM node:22.15 as builder

WORKDIR /client

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy rest of the files
COPY . .

COPY .env /client/.env

# Build the project
RUN npm run build

# stage2 as production
FROM nginx:alpine as production-build
COPY ./nginx.conf /etc/nginx/nginx.conf

## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

# Copy from stage 1
COPY --from=builder /client/dist /usr/share/nginx/html

ENTRYPOINT ["nginx", "-g", "daemon off;"]