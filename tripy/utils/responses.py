from rest_framework.response import Response


def success_response(data=None, message=None, status_code=None):
    return Response({
        "status": "success",
        "data": data,
        "message": message,
        "status_code": status_code
    })
