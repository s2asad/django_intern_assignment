from rest_framework.response import Response
from rest_framework import status


def get_object_or_404_custom(model, **kwargs):
    """Utility to fetch object or raise descriptive error."""
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def success_response(data, status_code=status.HTTP_200_OK):
    return Response({"success": True, "data": data}, status=status_code)


def error_response(message, status_code=status.HTTP_400_BAD_REQUEST, errors=None):
    payload = {"success": False, "message": message}
    if errors:
        payload["errors"] = errors
    return Response(payload, status=status_code)


def not_found_response(resource="Object"):
    return error_response(f"{resource} not found.", status.HTTP_404_NOT_FOUND)
