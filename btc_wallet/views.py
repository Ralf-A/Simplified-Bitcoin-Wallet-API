from django.http import JsonResponse

def notfound_handler(request, exception):
    """
    Custom 404 handler to return JSON response for Not Found errors.
    """
    return JsonResponse(
        {
            "error": "Page not found",
            "documentation": "https://github.com/Ralf-A/Simplified-Bitcoin-Wallet-API"
        },
        status=404
    )
