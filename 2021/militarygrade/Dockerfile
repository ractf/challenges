FROM alpine AS builder

RUN apk add --update go
RUN mkdir -p /opt
WORKDIR /opt
ADD main.go .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags '-extldflags "-static"' main.go

FROM scratch
COPY --from=0 /opt/main /
EXPOSE 80
ENTRYPOINT ["/main"]