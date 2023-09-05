# Multimodal Search on Iconclass using Vision-Language Models

This content is published on the URI: [https://demo.fiz-karlsruhe.de/iconclass/multimodal/index.html](https://demo.fiz-karlsruhe.de/iconclass/multimodal/index.html)


## Resources

This demo requires a database of images annotated with Iconclass codes and a FAISS index with the pre-computed CLIP embeddings for each image. If you are interested in the data to run this demo, you can use the [ICONCLASS forum](https://forum.iconclass.org/latest).

## Docker container

The container can be run using:

```shell
docker run -d -p 50000:80 --restart always --name ic_multimodal --network ise-net demo_multimodal
```

## Published APIs

It is possible to query the search engine through an open API available at [https://demo.fiz-karlsruhe.de/iconclass/multimodal/api/similarity_text](https://demo.fiz-karlsruhe.de/iconclass/multimodal/api/similarity_text), passing your query text as `q` parameter. The GET request will return the following json:

```
{
    "filenames":["IIHIM_RIJKS_786390193.jpg"],
    "ics":[
        ["25F23(LION)"]
        ],
    "labels":{
        "25F23(LION)": "beasts of prey, predatory animals: lion"
    }
}
```

You can access all the image files in IIIF using the following URI syntax: `https://iconclass.org/iiif/2/ + URI +/full/full/0/default.jpg`

Example: [https://iconclass.org/iiif/2/IIHIM_RIJKS_786390193.jpg/full/full/0/default.jpg](https://iconclass.org/iiif/2/IIHIM_RIJKS_786390193.jpg/full/full/0/default.jpg)