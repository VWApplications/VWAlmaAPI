FROM nginx:latest

COPY ./enviroments/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./project/staticfiles /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]