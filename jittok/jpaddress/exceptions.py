from ..exceptions import BaseError


class BaseJpaddressError(BaseError):
    ...


class ZipcodeNotFoundError(BaseJpaddressError, KeyError):
    ...
