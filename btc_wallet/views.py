from django.http import JsonResponse

handler404 = 'notfound_handler'
def notfound_handler(request, exception):
    # simple 404 handler
    return JsonResponse(
        {
            "error": "Page not found",
            "documentation": "https://github.com/Ralf-A/Simplified-Bitcoin-Wallet-API"
        },
        status=404
    )
