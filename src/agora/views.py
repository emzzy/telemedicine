import os
import time
import json

from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from .agora_key.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee
from pusher import Pusher
from users.models import UserAccount

# instantiate a Pusher Client
pusher_client = Pusher(
    app_id=os.environ.get('PUSHER_APP_ID',),
    key=os.environ.get('PUSHER_KEY'),
    secret=os.environ.get('PUSHER_SECRET'),
    ssl=True,
    cluster=os.environ.get('PUSHER_CLUSTER')
)

@login_required(login_url='/login/')
def index(request):
    #User = get_user_model()
    all_users = UserAccount.objects.exclude(id=request.user.id).only('id', 'first_name')
    return render(request, 'agora/index.html', {'allUsers': all_users})

def pusher_auth(request):
    print("🔹 Pusher authentication request received")
    print("🔹 Channel:", request.POST.get('channel_name'))
    print("🔹 Socket ID:", request.POST.get('socket_id'))
    print("🔹 User:", request.user if request.user.is_authenticated else "Not authenticated")
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=403)

    payload = pusher_client.authenticate(
        channel=request.POST['channel_name'],
        socket_id=request.POST['socket_id'],
        custom_data={
            'user_id': request.user.id,
            'user_info': {
                'id': request.user.id,
                'name': request.user.first_name
            }
        }
    )
    print("🔹 Authentication successful:", json.dumps(payload, indent=2))
    return JsonResponse(payload)

def generate_agora_token(request):
    try:
        print("🔹 Received token request")
        print("🔹 Request body:", request.body)

        # Extract Agora credentials
        appID = os.environ.get('AGORA_APP_ID')
        appCertificate = os.environ.get('AGORA_APP_CERTIFICATE')
        print(f"********Agora appID: {appID}********************************")

        if not appID or not appCertificate:
            print("❌ Missing Agora credentials")
            return JsonResponse({'error': 'Agora credentials not set'}, status=500)

        # Parse request body
        body = json.loads(request.body.decode('utf-8'))
        if 'channelName' not in body:
            print("❌ Missing channelName in request")
            return JsonResponse({'error': 'channelName is required'}, status=400)

        channelName = body['channelName']
        userAccount = request.user.first_name if request.user.is_authenticated else None
        if not userAccount:
            print("❌ User not authenticated")
            return JsonResponse({'error': 'User not authenticated'}, status=403)

        expireTimeInSeconds = 3600
        currentTimestamp = int(time.time())
        privilegeExpiredTs = currentTimestamp + expireTimeInSeconds

        print(f"🔹 Generating token for {userAccount} on channel {channelName}")

        token = RtcTokenBuilder.buildTokenWithAccount(
            appID, appCertificate, channelName, userAccount, Role_Attendee, privilegeExpiredTs
        )

        print("✅ Token generated successfully")
        return JsonResponse({'token': token, 'appID': appID})

    except json.JSONDecodeError:
        print("❌ Invalid JSON in request body")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"🚨 Unexpected error: {e}")
        return JsonResponse({'error': str(e)}, status=500)

# def generate_agora_token(request):
#     appID = os.environ.get('AGORA_APP_ID')
#     appCertificate = os.environ.get('AGORA_APP_CERTIFICATE')
#     channelName = json.loads(request.body.decode(
#         'utf-8'))['channelName']
#     userAccount = request.user.first_name
#     expireTimeInSeconds = 3600
#     currentTimestamp = int(time.time())
#     priviledgeExpiredTs = currentTimestamp + expireTimeInSeconds

#     token = RtcTokenBuilder.buildTokenWithAccount(
#         appID, appCertificate, channelName, userAccount, Role_Attendee, priviledgeExpiredTs
#     )
#     return JsonResponse({'token': token, 'appID': appID})

def call_user(request):
    body = json.loads(request.body.decode('utf-8'))

    user_to_call = body['user_to_call']
    channel_name = body['channel_name']
    caller = request.user.id

    pusher_client.trigger(
        'presence-online-channel',
        'make-agora-call',
        {
            'userToCall': user_to_call,
            'channel_name': channel_name,
            'from': caller
        }
    )
    return JsonResponse({'message': 'call has been placed'})