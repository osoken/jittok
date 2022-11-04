from ..exceptions import BaseError


class BaseJptextError(BaseError):
    ...


class UnknownEncodingError(BaseJptextError, ValueError):
    ...
