from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .healthbot import chatbot, reset

@csrf_exempt
def bot_reply(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        reply = chatbot(user_message)

        response = reply
        print("response: ",response)
        return JsonResponse({'message': response})

    return JsonResponse({'error': 'Invalid request method'})

def index(request):
    return render(request, 'index.html')

def faq(request):
    return render(request, 'FAQ.html')

def reset_app(request):
    # Reset the user messages
    print("Reset Called")
    reset()

    # Add any additional reset logic here

    return JsonResponse({'message': 'App reset successfully'})