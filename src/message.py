from datetime import datetime

class Message():
    def __init__(self, sender : str, message : str , room : str, timestamp : datetime = None, data : any = None):
        self.sender = sender
        self.message = message
        self.room = room
        if not timestamp:
            self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp

        self.data = data

    def to_dict(self):
        tmp_dict = {
            "from" : self.sender,
            "message" : self.message,
            "timestamp" : self.timestamp.strftime("%I:%M%p").lower(),
        }
        if self.data:
            tmp_dict["data"] = self.data.to_dict()
        return tmp_dict

    def __str__(self):
        return self.to_dict()