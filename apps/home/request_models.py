import json


class JsonBody:
    def to_json(self):
        return json.dumps(self.__dict__)


class UploadFileBody(JsonBody):
    def __init__(self, fileName, userName, userEmail):
        self.fileName = fileName
        self.userName = userName
        self.userEmail = userEmail


class GetInvoiceListBody(JsonBody):
    def __init__(self, userName, userEmail):
        self.userName = userName
        self.userEmail = userEmail


class GetInvoiceDetailsBody(JsonBody):
    def __init__(self, detailId, userName, userEmail):
        self.detailId = detailId
        self.userName = userName
        self.userEmail = userEmail
