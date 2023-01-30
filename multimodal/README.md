This can be run using the command:

```shell
docker run -d -p 50000:80 -v $(pwd)/Caddyfile:/etc/caddy/Caddyfile -v $(pwd)/www:/srv --restart always --name ic_multimodal --network ise-net caddy
```
