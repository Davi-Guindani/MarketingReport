import requests
import datetime as dt
from config import TOKEN

instagram_business_account_id = "17841401892691217"
api_version = "v15.0"

user_fields = ["biography", "followers_count", "follows_count", "media_count", "name", "username", "website"]
not_ranged_insights = ["audience_city", "audience_country", "audinece_gender_age", "audience_locale"]
teste = ["email_contacts", "follower_count", "get_directions_clicks", "impressions", "phone_call_clicks", "profile_views", "reach", "text_message_clicks", "website_clicks"]
ranged_insights = ["impressions"]
user_insights = not_ranged_insights + ranged_insights

class Info:
    def set_info (self):
        var = requests.get (self.build_url ())
        var = var.json ()
        var = self.clear_json (var)
        return var
    
    def show_info (self):
        print (self.set_info ())

class BasicInfo (Info):
    def __init__ (self, field):
        self.field = field 

    def build_url (self):
        url = "https://graph.facebook.com/" + api_version + "/" + instagram_business_account_id + "?fields=" + self.field + "&access_token=" + TOKEN
        return url

    def clear_json (self, var):
        del var ['id']
        return var

class InsightInfo (Info):
    def __init__ (self, metric):
        self.metric = metric
        self.period = "lifetime"

    def build_url (self):
        url = "https://graph.facebook.com/" + api_version + "/" + instagram_business_account_id + "/insights" + "?metric=" + self.metric + "&period=" + self.period + "&access_token=" + TOKEN
        return url

    def clear_json (self, var):
        del var['data'][0]['id']
        aux = var['data'][0]['values'][0]
        var['data'][0].pop ('values')
        var['data'][0].update (aux)
        return var
        
class RangedInsightInfo (InsightInfo):
    def __init__ (self, metric):
        super().__init__ (metric) 
        self.period = "day"

    def build_url (self, since, until):
        url = "https://graph.facebook.com/" + api_version + "/" + instagram_business_account_id + "/insights" + "?metric=" + self.metric + "&period=" + self.period + "&since=" + since + "&until=" + until + "&access_token=" + TOKEN
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

lista = []
for field in user_fields:
    lista.append (BasicInfo (field).set_info ())

for insight in user_insights:
    if insight in not_ranged_insights:
        lista.append (InsightInfo (insight).set_info ())
    if insight in ranged_insights:
        lista.append (RangedInsightInfo (insight).set_info ())

print (lista)
# for field in user_fields:
#     lista.update (BasicInfo (field).set_info ())
# print (lista)