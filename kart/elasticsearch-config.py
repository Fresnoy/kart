from haystack.backends.elasticsearch7_backend import (Elasticsearch7SearchEngine, Elasticsearch7SearchBackend,
                                                      Elasticsearch7SearchQuery)


class Elasticsearch71SearchBackend(Elasticsearch7SearchBackend):
    DEFAULT_SETTINGS = {
        "settings": {
            "index": {
                "max_ngram_diff": 2,
            },
            "analysis": {
                "analyzer": {
                    "ngram_analyzer": {
                        "tokenizer": "standard",
                        "filter": [
                            "haystack_ngram",
                            "lowercase",
                            "asciifolding",
                        ],
                    },
                    "edgengram_analyzer": {
                        "tokenizer": "standard",
                        "filter": [
                            "haystack_edgengram",
                            "lowercase",
                            "asciifolding",
                        ],
                    },
                },
                "filter": {
                    "haystack_ngram": {
                        "type": "ngram",
                        "min_gram": 3,
                        "max_gram": 4,
                    },
                    "haystack_edgengram": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 15,
                    },
                },
            },
        },
    }



class Elasticsearch71SearchEngine(Elasticsearch7SearchEngine):
    backend = Elasticsearch71SearchBackend
    query = Elasticsearch7SearchQuery
