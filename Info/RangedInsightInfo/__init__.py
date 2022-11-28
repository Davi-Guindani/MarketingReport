import datetime as dt
from Info.InsightInfo import InsightInfo
from config import TOKEN
import requests


class RangedInsightInfo(InsightInfo):
    def __init__ (self, metric):
        super().__init__ (metric) 
        self.period = "day"

    def build_url (self, since, until):
        url = "https://graph.facebook.com/" + self.api_version + "/" + self.instagram_business_account_id + "/insights" + "?metric=" + self.metric + "&period=" + self.period + "&since=" + since + "&until=" + until + "&access_token=" + TOKEN
        return url

    def clear_json (self, var):
        del var['data'][0]['id']
        aux = var['data'][0]['values'][0]
        var['data'][0].pop ('values')
        var['data'][0].update (aux)
        var['data'][0]['value'] = var['data'][0].pop ('value')
        del var['paging']
        return var

    def set_stamps (self, today, day):
        since = today - dt.timedelta (days = today.day - (day - 1))
        until = since + dt.timedelta (days = 1)
        since_stamp = dt.datetime.timestamp (since)
        until_stamp = dt.datetime.timestamp (until)
        return since_stamp, until_stamp

    def requests_loop (self, today, dic):
        for day in range (2, today.day + 1):
            since_stamp, until_stamp = self.set_stamps (today, day)
            var = requests.get (self.build_url (str (int (since_stamp)), str (int (until_stamp))))
            var = var.json ()
            var = self.clear_json (var)
            dic['impressions'].append (var['data'][0])
        return dic

    def set_info (self):
        dic = {'impressions' : []}
        today = dt.datetime.now ()
        return self.requests_loop (today, dic)