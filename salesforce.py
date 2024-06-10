from typing import Literal
import requests
from utils import make_dir, save_response_as_csv, merge_csv_files

class Salesforce:
    def __init__(self, environment:Literal["sandbox", "production"], username:str, password:str, client_id:str, client_secret:str, api_version:str = "v59.0"):

        self.environment = environment
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_version = api_version

        self.auth_url = None
        self.access_token = None
        self.instance_url = None
        self.id = None
        self.token_type = None
        self.issued_at = None
        self.signature = None   

        self.authenticate()

       
    def authenticate(self):
        if(self.environment == 'production'):
            self.auth_url = "https://login.salesforce.com/services/oauth2/token"
        elif(self.environment == 'sandbox'):
            self.auth_url = "https://test.salesforce.com/services/oauth2/token"
        else:
            self.auth_url = ""
        
        if not self.auth_url:
            raise ValueError("Invalid Environment")
        
        payload = f"""username={self.username}&password={self.password}&client_id={self.client_id}&client_secret={self.client_secret}&grant_type=password"""
    
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.post(self.auth_url, headers=headers, data=payload)
        if(response.status_code != 200):
            raise ValueError(str(response))
        
        response_json = response.json()
        self.access_token = response_json["access_token"]
        self.instance_url = response_json["instance_url"]+"/".strip()
        self.id = response_json["id"]
        self.token_type = response_json["token_type"]
        self.issued_at = response_json["issued_at"]
        self.signature = response_json["signature"]

    
    def get_object_data_using_query(self, query:str, object_name:str):
        if not self.access_token:
            self.authenticate()
        file_path = make_dir(object_name)
        service_url = f"services/data/{self.api_version}/query/?q="
        query_string = f"{service_url}{query}"
        headers = {
            "Authorization": "OAuth " + self.access_token
        }
        total_size = 0
        page_size = 0
        print("Process started to fetch records")
        while(True):
            object_url = self.instance_url + query_string
            response = requests.get(object_url, headers=headers)
            if(response.status_code == 200):
                response_json = response.json()
                total_size = response_json["totalSize"]
                page_size += len(response_json["records"])
                save_response_as_csv(response_json["records"], file_path, page_size)
                print(f"fetched {page_size} records of {total_size}")
                if(response_json["done"] == True):
                    break
                else:
                    query_string = response_json["nextRecordsUrl"]
            else:
                break
        merge_csv_files(file_path, object_name)