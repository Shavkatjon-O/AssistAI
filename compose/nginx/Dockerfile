FROM nginx:1.25.4-alpine

COPY ./default.conf /etc/nginx/conf.d/default.conf

COPY --from=web_django $APP_HOME/static /static