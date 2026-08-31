# Lightweight production Dockerfile for GCP Cloud Run or Docker hosting
FROM nginx:alpine

# Copy static web assets
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/
COPY portfolio_data.js /usr/share/nginx/html/
COPY portfolio_data.json /usr/share/nginx/html/
COPY assets/ /usr/share/nginx/html/assets/

# Configure custom Nginx port for GCP Cloud Run (supports dynamic $PORT, default 8080)
RUN printf 'server {\n\
    listen 8080;\n\
    server_name localhost;\n\
    location / {\n\
        root /usr/share/nginx/html;\n\
        index index.html;\n\
        try_files $uri $uri/ /index.html;\n\
    }\n\
}\n' > /etc/nginx/conf.d/default.conf

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
