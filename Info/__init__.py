import requests
from config import TOKEN
from abc import ABC,abstractclassmethod

# Super Classe, já contendo as informações do programa em forma de atributo estático
# Achei que para o caso de teste seria interessante, fiz dela abstrata herdando ABC(Abstract Base Class), e colocando seu __init__ como abstractclassmethod, o que faz com que ela seja não instanciável, mas seus filhos sim
class Info(ABC):
    instagram_business_account_id = "17841401892691217"
    api_version = "v15.0"

    user_fields = ["biography", "followers_count", "follows_count", "media_count", "name", "username", "website"]
    not_ranged_insights = ["audience_city", "audience_country", "audinece_gender_age", "audience_locale"]
    teste = ["email_contacts", "follower_count", "get_directions_clicks", "impressions", "phone_call_clicks", "profile_views", "reach", "text_message_clicks", "website_clicks"]
    ranged_insights = ["impressions"]
    user_insights = not_ranged_insights + ranged_insights

    @abstractclassmethod
    def __init__(self):
        pass

    def set_info (self):
        print(self.instagram_business_account_id)
        var = requests.get(self.build_url())
        var = var.json()
        var = self.clear_json(var)
        return var
    
    def show_info (self):
        print (self.set_info())

    def build_url (self):
        url = "https://graph.facebook.com/" + self.api_version + "/" + self.instagram_business_account_id + "?fields=" + self.field + "&access_token=" + TOKEN
        return url

    def clear_json (self, var):
        del var ['id']
        return var