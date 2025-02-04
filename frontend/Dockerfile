FROM nginx:alpine

# copy the built frontend files to the NGINX html dir
COPY build/ /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# start nginx
CMD [ "nginx", "-g", "daemon off;" ]