import json
import urllib.parse

from endpoints.requestObj import RequestObject
from models.bot.resources.message import MessageReference
from obj_types.proc_event import HttpEvent

class ChannelMessage(RequestObject):

    __slots__ = ('uri', 'headers', 'method', 'body')

    #-------------------------------------------------------------------------------------------
    def getChannelMessages(self, channelId, field="", messageId="", limit=50):
        allowedFields = ["around", "before", "after"]
        
        uri = f"/channels/{channelId}/messages"
        params = dict()

        if field and field not in allowedFields:
            raise ValueError(f"getChannelMessages() - Invalid field value: {field}")
        
        if field and not messageId:
            raise ValueError(f"getChannelMessages() - messageId required when field is provided")

        if field and messageId:
            params[field] = messageId
        
        if limit != 50:
            params["limit"] = limit

        uri = f"{uri}?{urllib.parse.urlencode(params)}"

    #-------------------------------------------------------------------------------------------
    def getChannelMessage(self, channelId, messageId):
        uri = f"/channels/{channelId}/messages/{messageId}"
        return self._to_request()

    #-------------------------------------------------------------------------------------------
    def createChannelMessage(self,
                            event,
                            content="",
                            nonce="",
                            tts=False,
                            embed=list(),
                            allowedMentions=None,
                            messageReference=None,
                            components=None,
                            stickerIds=list(),
                            payload_json="",
                            attachments=None):

        if not content and not embed and not stickerIds and not components:
            raise ValueError("createChannelMessage() - content, embed, stickerIds, or components required")

        self.uri = f"/channels/{event.channel_id}/messages"
        self.headers["Content-Type"] = "application/json"
        self.method = "POST"

        body = dict()

        if content:
            body["content"] = content
        if nonce:
            body["nonce"] = nonce
        if tts:
            body["tts"] = tts
        if embed:
            body["embed"] = embed
        if messageReference:
            body["message_reference"] = messageReference._to_dict()
        # not supported yet
        #if components:
        #    body["components"] = components
        if stickerIds:
            body["sticker_ids"] = stickerIds

        self.body = json.dumps(body)
        return self._to_request()

    #-------------------------------------------------------------------------------------------
    def createReaction(self, event, emoji=None):
        emojiEncoded = f'{emoji}'
        emojiEncoded = urllib.parse.quote(emojiEncoded)
        self.uri = f"/channels/{event.channel_id}/messages/{event.id}/reactions/{emojiEncoded}/@me"
        self.method = "PUT"
        return self._to_request()
    
    #-------------------------------------------------------------------------------------------
    def createChannelCrosspostMessage(self):
        pass

    #-------------------------------------------------------------------------------------------
    def createChannelMessageReaction(self):
        pass

    #-------------------------------------------------------------------------------------------
    def getChannelMessageReactions(self):
        pass

    #-------------------------------------------------------------------------------------------
    def editChannelMessage(self):
        pass

    #-------------------------------------------------------------------------------------------
    def deleteChannelMessage(self):
        pass