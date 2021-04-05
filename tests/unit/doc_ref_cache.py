import json
from os import listdir
from os.path import isfile, join
from docs import doc_ref

DOCS_CACHE_DIR = "/app/tests/data/docs_cache"


def refresh_doc_ref_cache():  # pragma: no cover
    files = doc_ref.curl_ref_files()
    for filename, content in files.items():
        with open(f"{DOCS_CACHE_DIR}/{filename}", "w") as file:
            txt = json.dumps(content, indent=4, sort_keys=True)
            file.write(txt)


def read_doc_ref_cache():
    cached = {}
    ref_filenames = [f for f in listdir(DOCS_CACHE_DIR) if isfile(join(DOCS_CACHE_DIR, f))]
    for ref_filename in ref_filenames:
        with open(f"{DOCS_CACHE_DIR}/{ref_filename}", "rt") as file:
            cached[ref_filename] = json.loads(file.read())
    return cached
