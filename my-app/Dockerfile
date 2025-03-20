FROM node:20.18.0-alpine AS builder 
WORKDIR /app 

COPY . . 
RUN npm install 


RUN npm run build

FROM node:20.18.0-alpine 
RUN npm install -g serve
WORKDIR /app 
COPY --from=builder /app/build /app  
EXPOSE 3000

CMD ["serve", "-s" ]