from rest_framework.response import Response
from .exceptions import TripyException, map_unknown_exception
import logging
import traceback
logger = logging.getLogger('django')


def custom_exception_handler(exc, context):
    if not isinstance(exc, TripyException):
        logger.error(
            "UNKNOWN EXCEPTION",
            extra={
                "unkown_exception": {
                    "message": str(exc),
                    "traceback": ''.join(traceback.format_tb(exc.__traceback__))
                }
            }
        )
        exc = map_unknown_exception(exc)

    return Response({
        "status": "error",
        "status_code": exc.code,
        "message": exc.message,
        "data": None
    }, status=exc.http_code)
