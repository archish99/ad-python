import hashlib

from django.http import HttpResponse
import json
# Create your views here.
from CommonUtils.httpProc import httpProc
from LoginSystem.models import BLUser
from UserProfile.models import UserProfile


def Dashboard(request):
    data = {}
    try:
         userID = request.session['userID']
    except:
        template = 'LoginSystem/Login.html'
        proc = httpProc(request, template, )
        return proc.render()
    user = BLUser.objects.get(pk=userID)
    try:
        userprofile = UserProfile.objects.get(owner=user)
    except:
        userprofile = UserProfile(owner=user)
        userprofile.save()

    data['ProfileImage'] = userprofile.image
    if(data['ProfileImage'] == ""):
        data['ProfileImage'] =  "https://www.gravatar.com/avatar/" + hashlib.md5(user.email.lower().encode()).hexdigest() + "?"
    else:
        data['ProfileImage'] = "http://127.0.0.1:8000/media/%s"%(userprofile.image)

    data['username'] = "%s %s"%(user.FirstName, user.LastName)

    code = request.GET.get('code', None)
    state = request.GET.get('state', None)

    if code != None:
        from google_auth_oauthlib.flow import Flow
        flow = Flow.from_client_secrets_file(
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

        ####



        # _SCOPE = "https://www.googleapis.com/auth/adwords"
        # _REDIRECT_URI = f"https://glimpse.cyberpanel.net/Login/gAds"
        #
        # flow = Flow.from_client_secrets_file('/home/glimpse.cyberpanel.net/public_html/client_secret.json',
        #                                      scopes=_SCOPE)
        # flow.redirect_uri = _REDIRECT_URI
        # # Pass the code back into the OAuth module to get a refresh token.
        # flow.fetch_token(code=code)
        # refresh_token = flow.credentials.refresh_token

        from google.ads.googleads.client import GoogleAdsClient

        credentialss = {
            "developer_token": "n5t26uhePod4OVCiNyVK_Q",
            "refresh_token": credentials.refresh_token,
            "client_id": "181170631609-j6v08sa4e3nfoolgb65r92lo3t2fgoc3.apps.googleusercontent.com",
            "client_secret": "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"}

        client = GoogleAdsClient.load_from_dict(credentialss)

        ga_service = client.get_service("GoogleAdsService")

        query = """
                SELECT
                  campaign.id,
                  campaign.name
                FROM campaign
                ORDER BY campaign.id"""

        # Issues a search request using streaming.
        stream = ga_service.search_stream(customer_id='123-456-7890', query=query)

        for batch in stream:
            for row in batch.results:
                return HttpResponse(f"Campaign with ID {row.campaign.id} and name "
                    f'"{row.campaign.name}" was found.')
                # print(
                #     f"Campaign with ID {row.campaign.id} and name "
                #     f'"{row.campaign.name}" was found.'
                # )

        return HttpResponse(credentials.refresh_token)

    template = 'BaseTemplates/Dashboard.html'
    proc = httpProc(request, template, data)
    return proc.render()

def GlobalAjax(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            if data['function'] == 'singupwith':
                from LoginSystem.views import singupwith
                return singupwith(request, data)
            elif data['function'] == 'FinishRegister':
                from LoginSystem.views import FinishRegister
                return FinishRegister(request, data)
            elif data['function'] == 'loginwith':
                from LoginSystem.views import loginwith
                return loginwith(request, data)
            elif data['function'] == 'loginwith2':
                from LoginSystem.views import loginwithfinal
                return loginwithfinal(request, data)
            elif data['function'] == 'SingUpEmail':
                from LoginSystem.views import SingUpEmail
                return SingUpEmail(request, data)
            elif data['function'] == 'LoginUserEmailPasswd':
                from LoginSystem.views import LoginUserEmailPasswd
                return LoginUserEmailPasswd(request, data)
            elif data['function'] == 'singupWalletconnect':
                from LoginSystem.views import singupWalletconnect
                return singupWalletconnect(request, data)
            elif data['function'] == 'FinshWalletConnectRegister':
                from LoginSystem.views import FinshWalletConnectRegister
                return FinshWalletConnectRegister(request, data)
            elif data['function'] == 'loginWalletconnect':
                from LoginSystem.views import loginWalletconnect
                return loginWalletconnect(request, data)
            elif data['function'] == 'loginWalletconnect2':
                from LoginSystem.views import loginWalletconnectfinal
                return loginWalletconnectfinal(request, data)
            elif data['function'] == 'signupFortmatic':
                from LoginSystem.views import signupFortmatic
                return signupFortmatic(request, data)
            elif data['function'] == 'FinshFortmaticRegister':
                from LoginSystem.views import FinshFortmaticRegister
                return FinshFortmaticRegister(request, data)
            elif data['function'] == 'loginFortmatic':
                from LoginSystem.views import loginFortmatic
                return loginFortmatic(request, data)
            elif data['function'] == 'loginFortmatic2':
                from LoginSystem.views import loginFortmaticfinal
                return loginFortmaticfinal(request, data)
            elif data['function'] == 'signupCoinbase':
                from LoginSystem.views import signupCoinbase
                return signupCoinbase(request, data)
            elif data['function'] == 'saveProfileData':
                from UserProfile.views import saveProfileData
                return saveProfileData(request, data)
            elif data['function'] == 'FetchProfileData':
                from UserProfile.views import FetchProfileData
                return FetchProfileData(request, data)
            elif data['function'] == 'Logout':
                from LoginSystem.views import Logout
                return Logout(request, data)
            elif data['function'] == 'GoogleAuthRedirect':
                from LoginSystem.views import GoogleAuthRedirect
                return GoogleAuthRedirect(request, data)

        else:
            return HttpResponse('hello')
    except BaseException as msg:
        proc = httpProc(request, None, None)
        return proc.ajax(0, str(msg))


