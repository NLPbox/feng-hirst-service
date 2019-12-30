# feng-hirst-service

[![Travis Build Status](https://travis-ci.org/NLPbox/feng-hirst-service.svg?branch=master)](https://travis-ci.org/NLPbox/feng-hirst-service)
[![Docker Build Status](https://img.shields.io/docker/cloud/build/nlpbox/feng-hirst-service.svg)](https://hub.docker.com/r/nlpbox/feng-hirst-service)

This docker container allows you to build, install and run the
[Feng/Hirst discourse parser](http://www.cs.toronto.edu/~weifeng/software.html)
(Feng and Hirst 2014) in a docker container with an added REST API.
Instead of the original code, this service uses [my fork](https://github.com/arne-cl/feng-hirst-rst-parser)
which applies some patches, is easier to dockerize and produces an output
format that is easier to parse (e.g. by [discoursegraphs](https://github.com/arne-cl/discoursegraphs)
or the [rst-converter-service](https://arne-cl@github.com/NLPbox/rst-converter-service)).

## build

docker build -t feng-hirst-service .

## run

docker run -p 8000:8000 -ti feng-hirst-service

## Usage Examples

### CURL

```
$ cat input_short.txt
Although they didn't like it, they accepted the offer.

$ curl -X POST -F "input=@input_short.txt" http://localhost:8000/parse
ParseTree('Contrast[S][N]', ["Although they did n't like it ,", 'they accepted the offer .'])
```

### Javascript

This works in Chrome, but not in Firefox:

```
>>> var xhr = new XMLHttpRequest();

>>> xhr.open("POST", "http://localhost:8000/parse")

>>> var data = new FormData();
>>> data.append('input', 'Altough they didn\'t like him, they accepted the offer.');

>>> xhr.send(data);
>>> console.log(xhr.response);
ParseTree('Background[S][N]', ["Altough they did n't like him ,", 'they accepted the offer .'])
```


## Citation

If you use the Feng/Hirst RST parser in your academic work, please cite the following paper:

Vanessa Wei Feng and Graeme Hirst, 2014.  
[A Linear-Time Bottom-Up Discourse Parser with Constraints and Post-Editing.](http://aclweb.org/anthology/P14-1048)  
In _Proceedings of the 52th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies (ACL-2014)_, Baltimore, USA. 

For more technical details, see:

Vanessa Wei Feng and Graeme Hirst, 2014.  
[Two-pass Discourse Segmentation with Pairing and Global Features.](http://arxiv.org/abs/1407.8215)  
arXiv:1407.8215v1.
