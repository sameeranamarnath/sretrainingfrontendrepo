# Use a Node.js image to build the Angular app
FROM node:alpine AS build



WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build --prod


# Use an Nginx image to serve the Angular app
#lightweight and efficient version 
FROM nginx:alpine

COPY --from=build /app/dist/employee-frontend-final /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

