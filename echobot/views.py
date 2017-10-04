# line_echobot/echobot/views.py

# WebhookHandler version

import random
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    print(event)
    userText = event.message.text
    print("siapa" in userText.lower())
    if "siapa" in userText.lower():
        groupId = event.source.group_id
        member_ids_res = line_bot_api.get_group_member_ids(groupId)
        userId = member_ids_res.member_ids[random.randint(0, member_ids_res.member_ids.length-1)]

        print(event.source.group_id)
        print(member_ids_res.member_ids.length)
        print(type(member_ids_res.member_ids))
        print(userId)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=groupId)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )


@handler.default()
def default(event):
    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Currently Not Support None Text Message')
    )


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
