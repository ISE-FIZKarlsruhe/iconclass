# Multimodal Search on Iconclass using Vision-Language Models

This content is published on the URI: [https://demo.fiz-karlsruhe.de/iconclass/multimodal/index.html](https://demo.fiz-karlsruhe.de/iconclass/multimodal/index.html)


## Resources

This demo requires a database of images annotated with Iconclass codes and a FAISS index with the pre-computed CLIP embeddings for each image. If you are interested in the data to run this demo, you can use the [ICONCLASS forum](https://forum.iconclass.org/latest).

## Docker container

The container can be run using:

```shell
docker run -d -p 50000:80 --restart always --name ic_multimodal --network ise-net demo_multimodal
```
