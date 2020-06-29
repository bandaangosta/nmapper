FROM alpine:latest
MAINTAINER Jose Ortiz jlortiz@uc.cl
RUN apk add nmap --no-cache && rm -f /var/cache/apk/*
ENTRYPOINT ["nmap"]