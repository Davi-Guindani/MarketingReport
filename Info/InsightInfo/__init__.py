from Info import Info
from config import TOKEN

class InsightInfo(Info):
    def __init__ (self, metric):
        self.metric = metric
        self.period = "lifetime"

    def build_url (self):
        url = "https://graph.facebook.com/" + self.api_version + "/" + self.instagram_business_account_id + "/insights" + "?metric=" + self.metric + "&period=" + self.period + "&access_token=" + TOKEN
        return url

    def clear_json (self, var):
        del var['data'][0]['id']
        aux = var['data'][0]['values'][0]
        var['data'][0].pop ('values')
        var['data'][0].update (aux)
        return var