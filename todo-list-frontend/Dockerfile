FROM node:18-alpine as builder
COPY package*.json ./
#RUN npm set progress=false && npm config set depth 0 && npm cache clean --force
## Storing node modules on a separate layer will prevent
## unnecessary npm installs at each build
# set working directory
WORKDIR /app
# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH
# install and cache app dependencies
COPY package.json /app/package.json
RUN npm install
RUN npm install -g @angular/cli@7.3.9
# add app
COPY . /app
# start app
CMD ng serve --proxy-config src/proxy.conf.json --host 0.0.0.0


#RUN npm install -g npm@7.24.0
#RUN npm i
#COPY . ./code
#RUN npm run build
#RUN npm run start



#RUN apk add --update python3 make g++ && rm -rf /var/cache/apk/*
