# Multimodal Search on Iconclass using Vision-Language Models

This content is published on the URI: [https://demo.fiz-karlsruhe.de/iconclass/multimodal/](https://demo.fiz-karlsruhe.de/iconclass/multimodal/)


## Docker container

This can be run using the command:

```shell
docker run -d -p 50000:80 -v $(pwd)/Caddyfile:/etc/caddy/Caddyfile -v $(pwd)/www:/srv --restart always --name ic_multimodal --network ise-net caddy
```
