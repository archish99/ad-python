import hashlib
import json
import os
from urllib.parse import unquote

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from CommonUtils.httpProc import httpProc
from LoginSystem.Authentication import Authentication
from LoginSystem.models import BLUser
from CommonUtils import randomPasswod
import requests


def Login(request):
    template = 'LoginSystem/Login.html'
    proc = httpProc(request, template, )
    return proc.render()


def signup(request):
    template = 'LoginSystem/signup.html'
    proc = httpProc(request, template, )
    return proc.render()


def singupwith(request, DataAjax):
    try:
        userPublicadress = DataAjax['Publicadress']
        WalletType = DataAjax['WalletType']

        WalletType = Authentication.FetchWalletType(WalletType)

        if WalletType == Authentication.Google:
            import jwt
            GoogleData = jwt.decode(userPublicadress, options={"verify_signature": False})
            try:
                bluser = BLUser.objects.get(email=GoogleData['email'])

            except:
                bluser = BLUser(email=GoogleData['email'], FirstName=GoogleData['name'],
                                LastName=GoogleData['family_name'], logintype=Authentication.Google)
                bluser.save()
            request.session['userID'] = bluser.pk
            proc = httpProc(request, None, None)
            return proc.ajax(1, None)

        elif WalletType == Authentication.Facebook:

            # try:
            #     bluser = BLUser.objects.get(email=GoogleData['email'])
            #
            # except:
            #     bluser = BLUser(email=GoogleData['email'], FirstName=GoogleData['name'],
            #                     LastName=GoogleData['family_name'], logintype=Authentication.Google)
            #     bluser.save()
            # request.session['userID'] = bluser.pk

            AccessToken = userPublicadress['authResponse']['accessToken']
            UserIDFB = userPublicadress['authResponse']['userID']
            url = f'https://graph.facebook.com/{UserIDFB}/accounts?access_token={AccessToken}'
            resp = requests.get(url)



            from facebook_business.adobjects.adaccount import AdAccount
            from facebook_business.adobjects.adsinsights import AdsInsights
            from facebook_business.api import FacebookAdsApi


            access_token = 'EAAISZCjqKQYkBADR1T5W3ZBlTGZACWeQxZAfzT27kCHJ6l7SiAH0OK0MFoEQVURwUZCcxpTNzyLr7Ssz5Ma1iIiLPDvAkfj7ZB4unk05stZBGv7aC3eGJukZBwcNt19OfjH7BPkJ6JKRroKNr3RSmuV9JN3qxtgDZBceVL5i6NnTdW127Pc843kqvaZCklCJyvVDAZD'
            ad_account_id = 'act_921174748850721'
            app_secret = '7df57195726e46cb4ecd266226ac2e1c'
            app_id = '583833066553737'
            FacebookAdsApi.init(app_id, app_secret, AccessToken)
            my_account = AdAccount('act_1024154661378169')
            campaigns = my_account.get_campaigns()

            GetAddAccts = f'https://graph.facebook.com/v14.0/{UserIDFB}/adaccounts?fields=name,id&access_token={AccessToken}'
            AddAccounts = json.loads(requests.get(GetAddAccts).text)

            for accounts in AddAccounts['data']:
                my_account = AdAccount(accounts['id'])

            ##

            UserIDForTestin = '10225316051921014'

            fields = [
                'results',
                'result_rate',
                'reach',
                'frequency',
                'impressions',
                'delivery',
                'spend',
                # 'impressions_gross',
                # 'impressions_auto_refresh',
                # 'attribution_setting',
                # 'quality_score_organic',
                # 'quality_score_ectr',
                # 'quality_score_ecvr',
                # 'cost_per_result',
                # 'cpp',
                # 'cpm',
                # 'actions:page_engagement',
                # 'actions:like',
                # 'actions:comment',
                # 'actions:post_engagement',
                # 'actions:post_reaction',
                # 'actions:onsite_conversion_post_save',
                # 'actions:post',
                # 'actions:photo_view',
                # 'actions:rsvp',
                # 'actions:checkin',
                # 'actions:full_view',
                # 'unique_actions:full_view',
                # 'ar_effect_share:ar_effect_share',
                # 'cost_per_action_type:page_engagement',
                # 'cost_per_action_type:like',
                # 'cost_per_action_type:post_engagement',
                # 'cost_per_action_type:rsvp',
                # 'actions:omni_add_to_cart',
                # 'actions:app_custom_event_fb_mobile_add_to_cart',
                # 'actions:offsite_conversion_fb_pixel_add_to_cart',
                # 'actions:offline_conversion_add_to_cart',
                # 'actions:onsite_conversion_add_to_cart',
                # 'unique_actions:omni_add_to_cart',
                # 'unique_actions:app_custom_event_fb_mobile_add_to_cart',
                # 'cost_per_unique_action_type:omni_add_to_cart',
                # 'cost_per_action_type:omni_add_to_cart',
                # 'action_values:omni_add_to_cart',
                # 'action_values:app_custom_event_fb_mobile_add_to_cart',
                # 'action_values:offsite_conversion_fb_pixel_add_to_cart',
                # 'action_values:offline_conversion_add_to_cart',
                # 'actions:omni_app_install',
                # 'actions:mobile_app_install',
                # 'actions:app_install',
                # 'cost_per_action_type:omni_app_install',
            ]
            params = {
                'time_range': {'since': '2022-07-29', 'until': '2022-08-28'},
                'filtering': [],
                'level': 'account',
                'breakdowns': [],
            }
            # resultAds  = AdAccount(ad_account_id).get_insights(
            #     fields=fields,
            #     params=params,
            # )

            # acfb = AdAccount(ad_account_id)
            #
            # resultAds = acfb.get_campaigns()

            proc = httpProc(request, None, None)
            return proc.ajax(0,str(AddAccounts['data']))

        else:

            try:
                bluser = BLUser.objects.get(PublicAdress=userPublicadress, logintype=WalletType)
                proc = httpProc(request, None, None)
                return proc.ajax(0, str("User already exists, please sign-in."))
            except:
                pass

            try:
                if WalletType == Authentication.MetaMask:
                    mkusr = BLUser(email='', FirstName='', LastName='', PublicAdress=userPublicadress,
                                   logintype=Authentication.MetaMask)
                    mkusr.save()
                    request.session['userID'] = mkusr.pk
                    proc = httpProc(request, None, None)
                    return proc.ajax(1, None)
                elif WalletType == Authentication.WalletConn:
                    mkusr = BLUser(PublicAdress=userPublicadress, email='', FirstName='', LastName='',
                                   logintype=Authentication.WalletConn)
                    mkusr.save()
                    request.session['userID'] = mkusr.pk
                    proc = httpProc(request, None, None)
                    return proc.ajax(1, None)
                elif WalletType == Authentication.Fortmatic:
                    mkusr = BLUser(PublicAdress=userPublicadress, email='', FirstName='', LastName='',
                                   logintype=Authentication.Fortmatic)
                    mkusr.save()
                    request.session['userID'] = mkusr.pk
                    proc = httpProc(request, None, None)
                    return proc.ajax(1, None)
                elif WalletType == Authentication.Coinbase_Wallet:
                    mkusr = BLUser(PublicAdress=userPublicadress, email='', FirstName='', LastName='',
                                   logintype=Authentication.Coinbase_Wallet)
                    mkusr.save()
                    request.session['userID'] = mkusr.pk
                    proc = httpProc(request, None, None)
                    return proc.ajax(1, None)
            except BaseException as msg:
                proc = httpProc(request, None, None)
                return proc.ajax(0, str(msg))
                # mkusr = BLUser.objects.get(PublicAdress=userPublicadress)
                #
                # request.session['userID'] = mkusr.pk
    except BaseException as msg:
        proc = httpProc(request, None, None)
        return proc.ajax(0, str(msg))


def RegisterFinish(request):
    UserID = request.session['userID']
    data = {}
    user = BLUser.objects.get(pk=UserID)
    data['UserID'] = UserID
    data['WalletType'] = user.logintype
    template = 'LoginSystem/RegisterMetamask.html'
    proc = httpProc(request, template, data)
    return proc.render()


def FinishRegister(request, DataAjax):
    try:
        ID = DataAjax['ID']
        WalletType = DataAjax['WalletType']
        email = DataAjax['email']
        lastname = DataAjax['lastname']
        firstname = DataAjax['firstname']

        usrobj = BLUser.objects.get(pk=ID)
        usrobj.email = email
        usrobj.FirstName = firstname
        usrobj.LastName = lastname

        usrobj.save()

        proc = httpProc(request, None, None)
        return proc.ajax(1, None)
    except BaseException as msg:
        proc = httpProc(request, None, None)
        return proc.ajax(0, str(msg))


def loginwith(request, DataAjax):
    try:
        Publicadress = DataAjax['Publicadress']
        WalletType = DataAjax['WalletType']
        if WalletType == 'Metamask':
            WalletType = Authentication.MetaMask
        elif WalletType == 'Wallet_Connect':
            WalletType = Authentication.WalletConn
        elif WalletType == 'Fortmatic':
            WalletType = Authentication.Fortmatic
        elif WalletType == 'Coinbase':
            WalletType = Authentication.Coinbase_Wallet

        Nonce = randomPasswod.generate_pass(5)

        try:
            usrobj = BLUser.objects.get(PublicAdress=Publicadress, logintype=WalletType)
            config = {}
            config['Nonce'] = Nonce
            config1 = json.dumps(config)
            usrobj.config = config1
            usrobj.save()
            data = {}
            request.session['userID'] = usrobj.pk
            data['userID'] = request.session['userID']

            data['Nonce'] = Nonce
            proc = httpProc(request, None, None)
            return proc.ajax(1, data)
        except:
            proc = httpProc(request, None, None)
            return proc.ajax(0, str('User Not Found'))
    except BaseException as msg:
        proc = httpProc(request, None, None)
        return proc.ajax(0, str(msg))

def loginwithfinal(request, DataAjax):
    try:
        UserID = DataAjax['UserID']
        signature = DataAjax['signature']
        account = DataAjax['account']
        Nonce = DataAjax['Nonce']

        from web3 import Web3

        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/abe9d79545a7417d8481f6d5846a3f7a'))
        # result = w3.eth.get_block('latest')
        #
        # print(result)

        # balance = w3.eth.get_balance(account)
        # (balance)

        from eth_account.messages import encode_defunct
        message = encode_defunct(text=Nonce)
        localaccount = w3.eth.account.recover_message(message, signature=signature)

        if localaccount.lower() == account.lower():
            proc = httpProc(request, None, None)
            return proc.ajax(1, None)
        else:
            proc = httpProc(request, None, None)
            return proc.ajax(0, str('Account not fetched'))
    except BaseException as msg:
        proc = httpProc(request, None, None)
        return proc.ajax(0, str(msg))

def GoogleAuthRedirect(request, DataAjax):
    try:

        # from google_auth_oauthlib.flow import Flow
        #
        # _SCOPE = "https://www.googleapis.com/auth/adwords"
        # _REDIRECT_URI = f"https://glimpse.cyberpanel.net/Login/gAds"
        #
        # flow = Flow.from_client_secrets_file('/home/glimpse.cyberpanel.net/public_html/client_secret.json', scopes=_SCOPE)
        # flow.redirect_uri = _REDIRECT_URI
        #
        # # Create an anti-forgery state token as described here:
        # # https://developers.google.com/identity/protocols/OpenIDConnect#createxsrftoken
        # passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()
        #
        # authorization_url, state = flow.authorization_url(
        #     access_type="offline",
        #     state=passthrough_val,
        #     prompt="consent",
        #     include_granted_scopes="true",
        # )

        import google.oauth2.credentials
        import google_auth_oauthlib.flow

        # Use the client_secret.json file to identify the application requesting
        # authorization. The client ID (from that file) and access scopes are required.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            '/home/glimpse.cyberpanel.net/public_html/client_secret.json',
            ['https://www.googleapis.com/auth/adwords'])


        flow.redirect_uri = 'https://glimpse.cyberpanel.net/Login/gAds'

        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true',
            prompt='consent'
        )
        request.session['state'] = state

        proc = httpProc(request, None, None)
        return proc.ajax(1, authorization_url)
    except BaseException as msg:
        proc = httpProc(request, None, None)
        return proc.ajax(0, str(msg))


#####.................................Email

def SingUpEmail(request, DataAjax):
    try:
        Firstname = DataAjax['Firstname']
        lastname = DataAjax['lastname']
        email = DataAjax['email']
        password = DataAjax['password']
        mkusr = BLUser(email=email, FirstName=Firstname, LastName=lastname, password=password,
                       logintype=Authentication.Email_password)
        mkusr.save()
        proc = httpProc(request, None, None)
        return proc.ajax(1, None)
    except BaseException as msg:
        proc = httpProc(request, None, None)
        return proc.ajax(0, str(msg))


def LoginUserEmailPasswd(request, DataAjax):
    try:

        email = DataAjax['email']
        password = DataAjax['password']
        try:
            getusr = BLUser.objects.get(email=email)
            usrpsswd = getusr.password
            if password == usrpsswd:
                request.session['userID'] = getusr.pk
            else:
                proc = httpProc(request, None, None)
                return proc.ajax(0, str("Password Not Matched!"))
        except BaseException as msg:
            proc = httpProc(request, None, None)
            return proc.ajax(0, str("Email Not find!"))
        proc = httpProc(request, None, None)
        return proc.ajax(1, None)
    except BaseException as msg:
        proc = httpProc(request, None, None)
        return proc.ajax(0, str(msg))


####.......................Logout
def Logout(request, DataAjax):
    try:
        userID = request.session['userID']
        del request.session['userID']
        proc = httpProc(request, None, None)
        return proc.ajax(1, None)
    except BaseException as msg:
        proc = httpProc(request, None, None)
        return proc.ajax(0, str(msg))


def gAds(request):
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)
    if code != None:
        # from google_auth_oauthlib.flow import Flow
        # flow = Flow.from_client_secrets_file(
        #     '/home/glimpse.cyberpanel.net/public_html/client_secret.json',
        #     scopes=['https://www.googleapis.com/auth/adwords'],
        #     state=state)
        #
        # flow.redirect_uri = 'https://glimpse.cyberpanel.net/Login/gAds'
        #
        # authorization_response = request.get_raw_uri()
        # flow.fetch_token(authorization_response=authorization_response)

        # Store the credentials in the session.
        # ACTION ITEM for developers:
        #     Store user's access and refresh tokens in your data store if
        #     incorporating this code into your real app.

        # credentials = flow.credentials

        ####

        # _SCOPE = "https://www.googleapis.com/auth/adwords"
        # _REDIRECT_URI = f"https://glimpse.cyberpanel.net/Login/gAds"
        #
        # flow = Flow.from_client_secrets_file('/home/glimpse.cyberpanel.net/public_html/client_secret.json',
        #                                      scopes=_SCOPE)
        #
        # flow.redirect_uri = _REDIRECT_URI
        # # Pass the code back into the OAuth module to get a refresh token.
        # # code = unquote(get_authorization_code(passthrough_val))
        # flow.fetch_token(code=code)
        # refresh_token = flow.credentials.refresh_token
        #return HttpResponse(refresh_token)

        import google.oauth2.credentials
        import google_auth_oauthlib.flow

        #state = request.session['state']
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            '/home/glimpse.cyberpanel.net/public_html/client_secret.json',
            scopes=['https://www.googleapis.com/auth/adwords'],
            state=state)

        flow.redirect_uri = 'https://glimpse.cyberpanel.net/Login/gAds'

        authorization_response = request.get_raw_uri()
        flow.fetch_token(authorization_response=authorization_response)

        # Store the credentials in the session.
        # ACTION ITEM for developers:
        #     Store user's access and refresh tokens in your data store if
        #     incorporating this code into your real app.

        credentials = flow.credentials

        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

        # from google.ads.googleads.client import GoogleAdsClient
        #
        # credentialss = {
        #     "developer_token": "n5t26uhePod4OVCiNyVK_Q",
        #     "refresh_token": credentials.refresh_token,
        #     "client_id": "181170631609-j6v08sa4e3nfoolgb65r92lo3t2fgoc3.apps.googleusercontent.com",
        #     "client_secret": "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",
        #     "login_customer_id": "1411331635"
        # }
        #
        # client = GoogleAdsClient.load_from_dict(credentialss)
        #client = GoogleAdsClient.load_from_storage("/home/glimpse.cyberpanel.net/public_html/google-ads.yaml")

        #return HttpResponse(str(refresh_token))

        # ga_service = client.get_service("GoogleAdsService")
        #
        # query = """
        #         SELECT
        #           campaign.id,
        #           campaign.name
        #         FROM campaign
        #         ORDER BY campaign.id"""
        #
        # # Issues a search request using streaming.
        # stream = ga_service.search_stream(customer_id='115-505-4364', query=query)
        # return HttpResponse(str(stream))
        #
        #
        #
        # for batch in stream:
        #     for row in batch.results:
        #         return HttpResponse(f"Campaign with ID {row.campaign.id} and name "
        #                             f'"{row.campaign.name}" was found.')
        #         # print(
        #         #     f"Campaign with ID {row.campaign.id} and name "
        #         #     f'"{row.campaign.name}" was found.'
        #         # )

        # ga_service = client.get_service("GoogleAdsService", version="v8")
        # query = "SELECT campaign.name FROM campaign LIMIT 10"
        # response = ga_service.search_stream(customer_id='115-505-4364', query=query)
        # Access the iterator in the same scope as where the service object was created.
        # try:
        #     hey = ''
        #     for batch in response:
        #         for row in batch.results:
        #             hey += f'"{row.campaign.name}" was found.'
        #     return HttpResponse(hey)
        # except BaseException as msg:
        #     return HttpResponse(str(msg))
        # Successfully iterate through response.

        url = f'https://www.googleapis.com/oauth2/v3/token'
        result = requests.post(url, data={"grant_type":"refresh_token","refresh_token": credentials.refresh_token, "client_id": "181170631609-j6v08sa4e3nfoolgb65r92lo3t2fgoc3.apps.googleusercontent.com", "client_secret": "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"})
        result = json.loads(result.text)
        access_token = result['access_token']
        #return HttpResponse(result.text)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'developer-token': "n5t26uhePod4OVCiNyVK_Q"
        }
        ## This part get customers for account authenticated above
        url = f'https://googleads.googleapis.com/v11/customers:listAccessibleCustomers'
        # result = requests.get(url,headers=headers)

        ### This will get details of selected account above
        url = f'https://googleads.googleapis.com/v11/customers/1411331635/googleAds:search'

        query = """
                SELECT
                    customer.id,
                    customer.descriptive_name,
                    customer.currency_code,
                    customer.time_zone,
                    customer.tracking_url_template,
                    customer.auto_tagging_enabled
                FROM customer
                LIMIT 1"""

        data = {'pageSize': 1000, "query": query}
        result = requests.post(url, headers=headers, data=data)

        #print(result.text)
        return HttpResponse(result.text)

        # return HttpResponse(credentials.refresh_token)