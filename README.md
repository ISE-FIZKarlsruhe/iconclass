# ICONCLASS Projects

Various projects done by the ISE group related to [ICONCLASS](https://icocnlass.org)

- Multimodal Search paper submission, January 2023

## Platform notes

The following setting is used on the `demo` nginx container to proxy all iconclass requests.

```
server {
  listen 80 ;
  server_name demo.fiz-karlsruhe.de;
  root /var/www/html;
  location /iconclass {
    allow  all;
    proxy_redirect     off;
    proxy_set_header    Host      $host;
    proxy_set_header    X-Real-IP    $remote_addr;
    proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
    client_max_body_size  500m;
    client_body_buffer_size 128k;
    proxy_connect_timeout  90;
    proxy_send_timeout   600;
    proxy_read_timeout   600;
    proxy_buffers      32 4k;
    proxy_pass http://ic_multimodal/iconclass;
  }
```
