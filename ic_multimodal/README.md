This can be run using the command:

```shell
docker run -p 50000:50000 -v $(pwd)/Caddyfile:/etc/caddy/Caddyfile -v $(pwd)/www:/srv --restart=always caddy
```
