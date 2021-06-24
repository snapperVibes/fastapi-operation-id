import copy

from fastapi import FastAPI
import pytest

from fastapi_operation_id import clean_ids, FastAPIOperationIDException, IDAlreadyExists


def test_():
    app = FastAPI()

    @app.get("/")
    def hello_world():
        return "Hello, world"

    # Sanity check
    assert (
        app.openapi()["paths"]["/"]["get"]["operationId"] == "hello_world__get"
    ), "The tests failed a sanity check; the schema without any modifications was not the expected outcome"

    @app.get("/double")
    def get_operation():
        pass

    @app.post("/double")
    def post_operation():
        pass

    @app.get("/normalize")
    def Ñ():
        pass

    @app.get("/your_own_id", operation_id="my_name")
    def this_name_is_overwritten():
        pass

    clean_ids(app)

    assert app.openapi()["paths"]["/"]["get"]["operationId"] == "hello_world"
    assert app.openapi()["paths"]["/double"]["get"]["operationId"] == "get_operation"
    assert app.openapi()["paths"]["/double"]["post"]["operationId"] == "post_operation"
    assert app.openapi()["paths"]["/normalize"]["get"]["operationId"] == "_"
    assert app.openapi()["paths"]["/your_own_id"]["get"]["operationId"] == "my_name"
    # Nothing should change if ran again
    cleaned_openapi = app.openapi()
    clean_ids(app)
    double_cleaned_openapi = app.openapi()
    assert cleaned_openapi == double_cleaned_openapi

    @app.post("/oh_no")
    def get_operation():
        pass

    with pytest.raises(FastAPIOperationIDException):
        clean_ids(app)

    with pytest.raises(IDAlreadyExists):
        clean_ids(app)


if __name__ == "__main__":
    pytest.main()
