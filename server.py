'''api server'''

import falcon

from utils import JSONTranslator
import channels

class Home(object):
    def on_get(self, req, resp):
        """
        Easily test if server is alive/find readme
        """
        response = "https://github.com/nielsds/kiosk-server"
        resp.status = falcon.HTTP_200
        resp.context["response"] = {"Kiosk-server": response}

class Channels(object):
    def on_get(self, req, resp):
        """
        Channels returns a list of all channels
        """
        response = CHANNELS.channels
        resp.status = falcon.HTTP_200
        resp.context["response"] = {"channels": response}

class Channel(object):
    """
    Get a list of all channels
    Post new channel data to a new or existing channel
    Delete an exisiting channel
    """
    def on_get(self, req, resp):
        """
        Channels returns an existing channels data (200)
        Returns an error if channel does not exist (404)
        or "channel" is missing from request (400)
        """
        request = (req.context['request'])
        if not request:
            response = 'Malformed request. Require keyword "channel".'
            resp.status = falcon.HTTP_400
        elif not 'channel' in request:
            response = 'Malformed request. Require key "channel".'
            resp.status = falcon.HTTP_400
        else:
            _channels = CHANNELS.channels
            if not request['channel'] in _channels:
                response = 'Unknown channel ' + request['channel']
                resp.status = falcon.HTTP_404
            else:
                response = _channels[request['channel']]
                resp.status = falcon.HTTP_200
        resp.context["response"] = {"channel": response}

    def on_post(self, req, resp):
        """
        Channels creates a new channel or updates an existing channels data (200)
        Returns an error if channel does not exist (404)
        or "channel" or "pages" is missing from request (400)
        """
        request = (req.context['request'])
        if not request:
            response = 'Malformed request. Require "channel" and "pages".'
            resp.status = falcon.HTTP_400
        elif not 'channel' in request:
            response = 'Malformed request. Require key "channel".'
            resp.status = falcon.HTTP_400
        elif not 'pages' in request:
            response = 'Malformed request. Require key "pages".'
            resp.status = falcon.HTTP_400
        else:
            CHANNELS.add(request['channel'], request['pages'])
            _channels = CHANNELS.channels
            response = _channels[request['channel']]
            resp.status = falcon.HTTP_200
        resp.context["response"] = {"channel": response}

    def on_delete(self, req, resp):
        """
        Channels deletes an existing channel (200)
        Returns an error if channel does not exist (404)
        or "channel" is missing from request (400)
        """
        request = (req.context['request'])
        if not request:
            response = 'Malformed request. Require "channel" and "pages".'
            resp.status = falcon.HTTP_400
        elif not 'channel' in request:
            response = 'Malformed request. Require key "channel".'
            resp.status = falcon.HTTP_400
        else:
            _channels = CHANNELS.channels
            if not request['channel'] in _channels:
                response = 'Unknown channel ' + request['channel']
                resp.status = falcon.HTTP_404
            else:
                CHANNELS.delete(request['channel'])
                response = 'Succesfully deleted channel "' + request['channel'] + '"'
                resp.status = falcon.HTTP_200
        resp.context["response"] = {"channel": response}

# Channels
CHANNELS = channels.Channels()

# Falcon
APP = falcon.API(middleware=[JSONTranslator()])
# Resource class instances
_HOME = Home()
_CHANNELS = Channels()
_CHANNEL = Channel()
# Falcon routes
APP.add_route("/", _HOME)
APP.add_route("/channels", _CHANNELS)
APP.add_route("/channel", _CHANNEL)
