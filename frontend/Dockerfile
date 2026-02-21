# based on the example given by the vuejs documentation : https://v2.vuejs.org/v2/cookbook/dockerize-vuejs-app.html?redirect=true


FROM node:25-alpine3.22 as build-stage

# install simple http server for serving static content
RUN npm install -g http-server

# make the 'app' folder the current working directory
WORKDIR /frontend

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# build app for production with minification
RUN npm run build

FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80:8080
CMD ["nginx", "-g", "daemon off;"]

