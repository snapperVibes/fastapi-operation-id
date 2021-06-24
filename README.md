# FastAPI Operation ID
##### A FastAPI utility for cleaner operation ids

Install using pip:
```shell
pip install fastapi-operation-id
```

## Usage


FastAPI Operation ID contains a single function, `clean_ids`.
```python
from fastapi import FastAPI
from fastapi_operation_id import clean_ids

app = FastAPI()


@app.get("/home")
def hello_world():
    return "Hello, world"

clean_ids(app)
```

Before `clean`, the operation id would is `hello_world_home_get`.

After `clean_app`, the operation id is `hello_world`.

## Why
Code generation on OpenAPI often use a route's operationId as the function name.
FastAPI defaults to operation IDs that, while descriptive, make poor function names.
FastAPI Operation ID changes the operation IDs to be human friendly.
