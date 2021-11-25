from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    FollowEvent, 
    UnfollowEvent,
    TextSendMessage, 
)
from farm.models import LinePush
from environs import Env 

env = Env() 
env.read_env()  

line_bot_api = LineBotApi(channel_access_token=env("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(channel_secret=env("LINE_CHANNEL_SECRET"))


@csrf_exempt
def callback(request):
    if request != 'POST':
        HttpResponseBadRequest()
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    except LineBotApiError:
        return HttpResponseBadRequest()
    return HttpResponse('OK', status=200)


@handler.add(FollowEvent)
def handle_follow(event):
    line_id = event.source.user_id
    profile = line_bot_api.get_profile(line_id)
    profile_name = profile.display_name
    profile_exists = LinePush.objects.filter(line_id=line_id).count() != 0
    if profile_exists:
        user_profile = LinePush.objects.get(line_id=line_id)
        user_profile.line_name = profile.display_name
        user_profile.line_picture_url = profile.picture_url
        user_profile.line_status_message = profile.status_message
        user_profile.unfollow = False
        user_profile.save()
    else:
        user_profile = LinePush(
            line_id = line_id,
            line_name = profile.display_name,
            line_picture_url = profile.picture_url,
            line_status_message = profile.status_message,
        )
        user_profile.save()
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='梨屋さん「日報アプリ」へようこそ！')
    )


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    line_id = event.source.user_id
    user_profile = LinePush.objects.get(line_id=line_id)
    user_profile.delete()


