# build
FROM node:20 as build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend/* ./app
RUN npm run build


# production
FROM nginx:latest as production

WORKDIR /app

RUN apk update && apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools &&\
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY --from=build /app/dist /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./backend /app

RUN pip install -r requirements.txt


CMD gunicorn -b 0.0.0.0:5000 run:app --daemon && \
      sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && \
      nginx -g 'daemon off;'

# Stage 1: Compile and Build angular codebase

# Use official node image as the base image
# FROM node:latest as build

# Set the working directory
# WORKDIR /app

# # Add the source code to app
# COPY ./LearnMath/frontend /app/

# # Install all the dependencies
# RUN npm install

# # Generate the build of the application
# RUN npm run build


# # Stage 2: Serve app with nginx server

# # Use official nginx image as the base image
# FROM nginx:latest

# # Copy the build output to replace the default nginx contents.
# COPY --from=build /usr/local/app/dist/sample-angular-app /usr/share/nginx/html

# # Expose port 80
# EXPOSE 80