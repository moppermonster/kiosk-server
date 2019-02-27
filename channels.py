'''Kiosk main functions and classes'''


class Channels():
    """
    Holds dict of channels
    Channels have a uuid name
    Channels contain a list of urls
    """

    def __init__(self):
        self.channels = {
            '_standby': ['https://dutchsec.com']
        }

    def add(self, name, pages):
        """
        Add a list of urls to pages
        pages = list of urls
        time = time before refresh in seconds
        """
        self.channels.update({name: pages})

    def delete(self, name):
        """
        Remove entry name from channels dict
        """
        if name in self.channels:
            del self.channels[name]
