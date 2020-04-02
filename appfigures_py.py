from rauth import OAuth1Session, OAuth1Service


class AppFigures(object):
    BASE_URL = "https://api.appfigures.com/v2"

    def __init__(self, client_key, client_secret, access_token=None, access_token_secret=None):
        self.client_key = client_key,
        self.client_secret = client_secret
        self.request_token_url = self.BASE_URL + "/oauth/request_token"
        self.authorize_url = self.BASE_URL + "/oauth/authorize"
        self.access_token_url = self.BASE_URL + "/oauth/access_token"

        self.session = self.get_session(access_token=access_token,access_token_secret=access_token_secret)

    def get_service(self):
        return OAuth1Service(name="appfigures",
                             consumer_key=self.client_key,
                             consumer_secret=self.client_secret,
                             request_token_url=self.request_token_url,
                             access_token_url=self.access_token_url,
                             authorize_url=self.authorize_url,
                             base_url=self.BASE_URL)

    def get_session(self, access_token=None, access_token_secret=None):
        oauth = self.get_service()

        if access_token:
            session = OAuth1Session(self.client_key, self.client_secret,
                                    access_token, access_token_secret,
                                    service=oauth)
            self.session = session
            return session

        params = {"oauth_callback": "oob"}
        headers = {'X-OAuth-Scope': 'public:read,products:read,private:read'}
        request_token, request_token_secret = oauth.get_request_token(
            params=params,
            headers=headers
        )

        authorization_url = oauth.get_authorize_url(request_token)
        print("Go here: %s to get your verification token."
              % authorization_url)
        verifier = raw_input("Paste verifier here: ")
        session = oauth.get_auth_session(request_token,
                                         request_token_secret,
                                         "POST",
                                         data={"oauth_verifier": verifier})
        return session

    def get_downloads(self, start_date, end_date, group_by='stores', granularity='daily'):
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'group_by': group_by,
            'granularity': granularity
        }

        resp = self.session.get(url=self.BASE_URL + '/reports/sales', params=params)
        return resp.json()

    def get_usage(self, start_date, end_date, group_by='network,date'):
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'group_by': group_by,
        }

        resp = self.session.get(url=self.BASE_URL + '/reports/usage', params=params)
        print(resp)
        return resp.json()