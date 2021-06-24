import re
from typing import Callable, Union

from fastapi import FastAPI, APIRouter
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from fastapi.utils import generate_operation_id_for_path


class FastAPIOperationIDException(Exception):
    pass


class IDAlreadyExists(FastAPIOperationIDException):
    def __init__(self, operation_id: str) -> None:
        self.args = (
            f"Each route's operation id must be unique. "
            f"'{operation_id}' is id for multiple routes. "
            f"Change its name to fix this error.",
        )


def _generate_clean_operation_id_for_path(*, name: str, path: str, method: str):
    return re.sub("[^0-9a-zA-Z_]", "_", name).lower()


def clean_ids(
    router: Union[FastAPI, APIRouter],
    operation_id_maker: Callable[
        [str, str, str], str
    ] = _generate_clean_operation_id_for_path,
) -> None:
    """
    Change a FastAPI app's routes' operation ids in place.

    :arg router
        The FastAPI router that will have its names cleaned
    :arg operation_id_maker
        A callable with the signature `(*, name: str, path: str, method: str) -> str`
        Each route's operation id is derived from this function.

    :raises IDAlreadyExists
    """
    number_of_routes = 0
    operation_ids = set()
    for route in router.routes:
        if type(route) != APIRoute:
            continue
        try:
            for method in route.methods:
                default_id = generate_operation_id_for_path(
                    name=route.name, path=route.path, method=method
                )
                print(route.operation_id, default_id)
                if (route.operation_id is not None) and (
                    route.operation_id != default_id
                ):
                    continue
                route.operation_id = operation_id_maker(
                    name=route.name, path=route.path, method=method
                )
        finally:
            operation_ids.add(route.operation_id)
            number_of_routes += 1
            if number_of_routes != len(operation_ids):
                raise IDAlreadyExists(route.operation_id)

    router.openapi_schema = get_openapi(
        title=router.title,
        version=router.version,
        openapi_version=router.openapi_version,
        description=router.description,
        routes=router.routes,
        tags=router.openapi_tags,
        servers=router.servers,
    )
