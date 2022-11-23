import requests
import datetime as dt
import calendar 

access_token = "EAALB2PWZBZBusBAGFopdC1yhb8EzMy1P9YSEzFQwYvEng4F6HrucXOJmCRksIZAME3dHnxGNZCgcjiapSsXR5kbZC68z0tBGTA9XpeL84zZCrPEtSiO6SrZBYsSCSJrtfhZBBZCZABF7jxjo5IHUF2QdYRr9JVmDZB9hzBgEeq0QqrtW3H8FZA7ZB3NUjr1zhocV8ocAZD"
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
}

def url_builder_basic_profile_infos (field):
    url = "https://graph.facebook.com/" + api_version + "/" + instagram_business_account_id + "?fields=" + field + "&access_token=" + access_token
    return url

def url_builder_profile_insights (metric, period):
    url = "https://graph.facebook.com/" + api_version + "/" + instagram_business_account_id + "/insights" + "?metric=" + metric + "&period=" + period + "&access_token=" + access_token
    return url

def url_builder_profile_insights_with_time (metric, period, since, until):
    url = "https://graph.facebook.com/" + api_version + "/" + instagram_business_account_id + "/insights" + "?metric=" + metric + "&period=" + period + "&since=" + since + "&until=" + until + "&access_token=" + access_token
    return url

def get_basic_profile_info (field):
    var = ""
    var = requests.get (url_builder_basic_profile_infos (field))
    var = var.json ()
    del var['id']
    return var

def get_profile_insight (metric, period):
    var = ""
    var = requests.get (url_builder_profile_insights (metric, period))
    var = var.json ()
    del var['data'][0]['id']
    return var

def get_profile_insight_with_time (metric, period, since, until):
    var = ""
    var = requests.get (url_builder_profile_insights_with_time (metric, period, since, until))
    var = var.json ()
    return var

for field in basic_info_fields:
    basic_infos.update (get_basic_profile_info (field))

for metric in insight_info_metrics:
    insight_infos['data'].append (get_profile_insight (metric, insight_info_metrics[metric])['data'][0])

for i in range (4):
    aux = insight_infos['data'][i]['values'][0]
    insight_infos['data'][i].pop ('values')
    insight_infos['data'][i].update (aux)
    insight_infos['data'][i]['values'] = insight_infos['data'][i].pop ('value')

today = dt.datetime.now ()
if today.day == 1:
    #mes todo
    print ("ignora")
else: 
    for day in range (2, today.day + 1):
        since = today - dt.timedelta (days = today.day - (day - 1))
        until = since + dt.timedelta (days = 1)
        since_stamp = dt.datetime.timestamp (since)
        until_stamp = dt.datetime.timestamp (until)
        teste = get_profile_insight_with_time ("impressions", "day", str (int (since_stamp)), str (int (until_stamp)))
        del teste['paging']
        insight_infos['data'].append (teste['data'][0])

print (insight_infos)