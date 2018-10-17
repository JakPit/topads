from locust import HttpLocust, TaskSet, task
from modules import topads
import random
import json

class TopadsFlashSale(TaskSet):
    def on_start(self):
        if not hasattr(TopadsFlashSale,'config_loaded'):
            TopadsFlashSale.config = self.configuration["production"]
            TopadsFlashSale.topads_config = self.load_config('squads/brown/configs/topads_config.json')
            TopadsFlashSale.config_loaded = True
        
        self.device_list = ["android" for _ in range(20)]
        self.device_list += ["ios" for _ in range(2)]
        self.device_list += ["mobile"]

    @task(1)
    def browse_home(self):
        #https://ta.tokopedia.com/promo/v1.1/display/ads?ep=product&item=4&src=home&device=android&page=1&user_id=16386956&dep_id=0&search_nf=0
        user_id = random.choice(TopadsFlashSale.topads_config["user_id"])
        device = random.choice(self.device_list)
        query = 'page=1&search_nf=0&ep=product&src=home&'
        _ = topads.promo_display_ads_v1_1(self, topads.host_production,
                                            query=query + "user_id=" + user_id + "&device=" + device,
                                            name=topads.host_production + "/promo/v1.1/display/ads?ep=product&item=4&src=home")
        
    @task(1)
    def headline_home(self):
        user_id = random.choice(TopadsFlashSale.topads_config["user_id"])
        device = random.choice(self.device_list)
        query = 'ep=cpm&item=1&src=home&template_id=6&'
        _ = topads.promo_display_ads_v1_1(self, topads.host_production,
                                            query=query + "user_id=" + user_id + "&device=" + device,
                                            name=topads.host_production + "/promo/v1.1/display/ads?ep=cpm&item=1&src=home")
       

    @task(1)
    def topads_pdp(self):
        user_id = random.choice(TopadsFlashSale.topads_config["user_topads_pdp"])
        device = random.choice(self.device_list)
        query = 'ep=product&item=5&src=pdp&'
        xparam = random.choice(list(TopadsFlashSale.topads_config["product_topads_pdp"]))
        xparamstring = json.dumps(xparam)
        _ = topads.promo_display_ads_v1_1(self, topads.host_production, 
                                            query=query + "user_id=" + user_id +  "&device=" + device + "&xparams=" + xparamstring,
                                            name=topads.host_production+"/promo/v1.1/display/ads?src=pdp")


class WebsiteUser(HttpLocust):
    host = ""
    task_set = TopadsFlashSale  
    min_wait = 1000
    max_wait = 1500