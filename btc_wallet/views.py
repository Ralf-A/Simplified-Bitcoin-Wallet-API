from django.http import JsonResponse

handler404 = 'notfound_handler'
def notfound_handler(request, exception):
    return JsonResponse(
        {
            "error": "Page not found",
            "documentation": "https://github.com/Ralf-A/Simplified-Bitcoin-Wallet-API"
        },
        status=404
    )
