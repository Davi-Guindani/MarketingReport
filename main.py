import requests
import datetime as dt
from config import TOKEN

access_token = TOKEN
instagram_business_account_id = "17841401892691217"
api_version = "v15.0"

basic_infos = {}
basic_info_fields = ["biography", "followers_count", "follows_count", "media_count", "name", "username", "website"]

insight_infos = {'data' : []}
insight_info_metrics = {
    "audience_city" : "lifetime",
    "audience_country" : "lifetime",
    "audience_gender_age" : "lifetime",
    "audience_locale" : "lifetime"
    #"impressions" : "day"
    #"followers" : "day"
}

def url_builder_basic_profile_infos (field):
    url = "https://graph.facebook.com/" + api_version + "/" + instagram_business_account_id + "?fields=" + field + "&access_token=" + access_token
    return url

def url_builder_profile_insights (metric, period, *args):
    if (len (args) == 0):
        url = "https://graph.facebook.com/" + api_version + "/" + instagram_business_account_id + "/insights" + "?metric=" + metric + "&period=" + period + "&access_token=" + access_token
    else:
        url = "https://graph.facebook.com/" + api_version + "/" + instagram_business_account_id + "/insights" + "?metric=" + metric + "&period=" + period + "&since=" + args[0] + "&until=" + args[1] + "&access_token=" + access_token
    return url

def clear_json (var, info_type):
    match info_type:
        case "basic":
            del var['id']
        case "insisght":
            del var['data'][0]['id']
            aux = var['data'][0]['values'][0]
            var['data'][0].pop ('values')
            var['data'][0].update (aux)
            var['data'][0]['value'] = var['data'][0].pop ('value')
        case _:
            return
    return var

def get_basic_profile_info (field):
    var = ""
    var = requests.get (url_builder_basic_profile_infos (field))
    var = var.json ()
    var = clear_json (var, "basic")
    return var

def get_profile_insight (metric, period, *args):
    var = ""
    var = requests.get (url_builder_profile_insights (metric, period, *args))
    var = var.json ()
    var = clear_json (var, "insisght")
    return var

for field in basic_info_fields:
    basic_infos.update (get_basic_profile_info (field))

for metric in insight_info_metrics:
    insight_infos['data'].append (get_profile_insight (metric, insight_info_metrics[metric])['data'][0])

today = dt.datetime.now ()
insight_infos['data'].append ({'impressions' : []})

for day in range (1, today.day + 1):
    since = today - dt.timedelta (days = today.day - (day - 1))
    until = since + dt.timedelta (days = 1)
    since_stamp = dt.datetime.timestamp (since)
    until_stamp = dt.datetime.timestamp (until)
    teste = get_profile_insight ("impressions", "day", str (int (since_stamp)), str (int (until_stamp)))
    del teste['paging']
    insight_infos['data'][4]['impressions'].append (teste['data'][0])

# print (basic_infos)
print (insight_infos)