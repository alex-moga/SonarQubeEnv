import requests
import logging
import sys
import json

class HttpClient:

    def __init__(self, base_url):
        self.base_url = base_url

    def upload_file_request(self, api_url, files):
        try:
            request_url = self.base_url + api_url
            response = requests.post(request_url, files=files, auth=('admin', 'admin'))
        except requests.exceptions.HTTPError as err:
            print('Failed send file request to SonarQube API: ' + request_url)
            print('Response is: {content}'.format(content=err.response.content))

    def send_param_request(self, api_url, params):
        try:
            request_url = self.base_url + api_url
            response = requests.post(request_url, params=params, auth=('admin', 'admin'))
	    return response.content
        except requests.exceptions.HTTPError as err:
            print('Failed send param request to SonarQube API: ' + request_url)
            print('Response is: {content}'.format(content=err.response.content))


class SonarQubeAPI:

    def __init__(self, base_url):
        self.hcl = HttpClient(base_url)

    def set_sonar_quality_profile(self, snq_profile_file):
        logging.info("Config quality profile: " + snq_profile_file)
        files = {
           'backup': (snq_profile_file, open(snq_profile_file, 'rb'))
        }
        self.hcl.upload_file_request('/api/qualityprofiles/restore', files)

    def mark_default_quality_profile(self, profile_name):
        logging.info("Makes default quality profile: " + profile_name)
        params = (
            ('language', 'java'),
            ('profileName', profile_name)
        )
        self.hcl.send_param_request('/api/qualityprofiles/set_default', params)

    def create_quality_gate(self, gate_name, metrics):
        logging.info("Config quality gate " + gate_name + " using metrics: " + str(metrics)) 
        self.hcl.send_param_request('/api/qualitygates/destroy', {'id' : 1}) 
        self.hcl.send_param_request('/api/qualitygates/create', {'name' : gate_name}) 
        self.hcl.send_param_request('/api/qualitygates/select_as_default', { 'id' : 2 })
        for m in metrics:
             logging.info("append metric " + m + " to " + gate_name)
             params = (
                 ('gateId', 2),
                 ('metric', m),  
                 ('op', 'GT'),
                 ('error', 0)
             )
             self.hcl.send_param_request('/api/qualitygates/create_condition', params)


    def create_user(self, login, name, password):
        logging.info("append user " + login);
        params = (
            ('login', login),
            ('password', password),
            ('password_confirmation', password),
            ('name', 'Sonar qube work user')
        )
        self.hcl.send_param_request('/api/users/create', params) 

    
    def revoke_token(self, token_name):
        logging.info("revoke token for " + token_name)
        params = (
            ('name', token_name),
            ('login', token_name)
        )
        self.hcl.send_param_request('/api/user_tokens/revoke', params)


    def chek_token_exists(self, token_name):
        resp_str = self.hcl.send_param_request('/api/user_tokens/search', {'login' : token_name})
        response = json.loads(resp_str)
        user_tokens = {k:v for k,v in response.items() if k == "userTokens"} 
	token_exists_flag = bool(len(next(iter(user_tokens.itervalues()), None)))
        if token_exists_flag:
            logging.info("token exists!")
        
        return token_exists_flag
	
    def generate_tooken(self, token_name):
        logging.info("generate token for " + token_name);
        params = (
            ('name', token_name),
            ('login', token_name)
        )
	if self.chek_token_exists(token_name):
            self.revoke_token(token_name)
        response = self.hcl.send_param_request('/api/user_tokens/generate', params)
        print '*** tooken: ' + response 

    def enable_support(self):
        logging.info('enable organization support')
        self.hcl.send_param_request('/api/organizations/enable_support', {})


logging.basicConfig(level=logging.INFO)

if len(sys.argv) > 1:
    BASE_URL=sys.argv[1]
    logging.info('Sonar API endpoint: ' + BASE_URL)
else:  
    raise Exception('Missing base_url argument')

snq_api = SonarQubeAPI(BASE_URL)

#apply SonarQube profile
snq_api.set_sonar_quality_profile('./bin/java-git-qualityprofile.xml')
snq_api.mark_default_quality_profile('Dit_java_qa_profile')

#configurate quality gate 
snq_api.create_quality_gate('DitJavaSevirity', ('blocker_violations', 'critical_violations'))

#append work user and obtain his token
snq_api.create_user('sonar', 'Sonar qube work user', '357f1c8957')
snq_api.generate_tooken('sonar')

#enable organiztion support
snq_api.enable_support()
