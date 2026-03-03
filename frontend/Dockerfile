# based on the example given by the vuejs documentation : https://v2.vuejs.org/v2/cookbook/dockerize-vuejs-app.html?redirect=true


FROM node:25-alpine3.22 as build-stage

# install simple http server for serving static content
RUN npm install -g http-server

# make the 'app' folder the current working directory
WORKDIR /frontend

# allow build-time override of the backend URL so Vite can bake it into
# the compiled assets (`import.meta.env.VITE_BACKEND_URL`).  Default to the
# internal service name so that even if the build arg is omitted the frontend
# will target the backend container on the shared network.
ARG VITE_BACKEND_URL="http://backend:8000"
ENV VITE_BACKEND_URL=${VITE_BACKEND_URL}

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# build app for production with minification
RUN npm run build

FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /frontend/dist /usr/share/nginx/html

EXPOSE 80:8080
CMD ["nginx", "-g", "daemon off;"]

