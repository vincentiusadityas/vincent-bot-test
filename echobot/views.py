# line_echobot/echobot/views.py

# WebhookHandler version

import random
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

yesNo = ["iya", "ngga"]
groupDict = {}

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):

    userText = event.message.text

    groupId = event.source.group_id
    userId = event.source.user_id

    if groupId not in groupDict:
        groupDict[groupId] = [userId]
    else:
        groupDict[groupId].append(userId)

    if "siapa saya" in userText.lower():
        profile = line_bot_api.get_group_member_profile(groupId, event.source.user_id)
        name = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=name)
        )

    if "siapa" in userText.lower():
        profile = line_bot_api.get_group_member_profile(groupId, groupDict[groupId][random.randint(0, len(groupDict[groupId])-1)])
        name = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=name)
        )

    elif "apakah" in userText.lower():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=yesNo[random.randint(0,1)])
            )

    elif "main yuk" in userText.lower():
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='Menu',
                text='Please select',
                actions=[
                    PostbackTemplateAction(
                        label='postback',
                        text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message',
                        text='message text'
                    ),
                    URITemplateAction(
                        label='uri',
                        uri='http://example.com/'
                    )
                ]
            )
        )
        
        line_bot_api.reply_message(
            event.reply_token,
            buttons_template_message
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
