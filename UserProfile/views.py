import hashlib
import json

from django.shortcuts import render

from CommonUtils.httpProc import httpProc

# Create your views here.
from LoginSystem.models import BLUser
from UserProfile.models import UserProfile
from django.core.files.storage import FileSystemStorage


def Myprofile(request):
    try:
        try:
           userID =  request.session['userID']
        except:
            template = 'LoginSystem/Login.html'
            proc = httpProc(request, template, )
            return proc.render()

        data = {}
        user = BLUser.objects.get(pk=userID)
        userprofile = UserProfile.objects.get(owner=user)
        data['FirstName'] = user.FirstName
        data['LastName'] = user.LastName
        data['Email'] = user.email
        data['bio'] = userprofile.bio
        data['ProfileImage'] = userprofile.image
        if (data['ProfileImage'] == ""):
            data['ProfileImage'] = "https://www.gravatar.com/avatar/" + hashlib.md5(user.email.lower().encode()).hexdigest() + "?"
        else:
            data['ProfileImage'] = "http://127.0.0.1:8000/media/%s" % (userprofile.image)

        data['username'] = "%s %s" % (user.FirstName, user.LastName)

        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            DPname = myfile.name
            fs = FileSystemStorage()
            fs.save(myfile.name, myfile)
            userprofile.image = DPname
            userprofile.save()
            data['uploaded_file'] = True
            template = 'UserProfile/MyProfile.html'
            proc = httpProc(request, template, data)
            return proc.render()

        template = 'UserProfile/MyProfile.html'
        proc = httpProc(request, template, data)
        return proc.render()
    except BaseException as msg:
        print("Error:%s"%msg)

def saveProfileData(request, DataAjax):
    try:

        userID =  request.session['userID']
        UserBio = DataAjax ['userBio']
        firstname = DataAjax ['firstname']
        lastname = DataAjax ['lastname']
        userwebsite = DataAjax ['userwebsite']
        userphone = DataAjax ['userphone']
        companyname = DataAjax ['companyname']
        Facebook = DataAjax ['Facebook']
        Twitter = DataAjax ['Twitter']
        Instagram = DataAjax ['Instagram']
        Linkedin = DataAjax ['Linkedin']
        Skype = DataAjax ['Skype']
        Github = DataAjax ['Github']
        category = DataAjax ['category']

        social ={}

        social['Facebook'] = Facebook
        social['Twitter'] = Twitter
        social['Instagram'] = Instagram
        social['Linkedin'] = Linkedin
        social['Skype'] = Skype
        social['Github'] = Github

        config = {}
        config['userphone'] = userphone
        config['companyname'] = companyname
        config['userwebsite'] = userwebsite


        user = BLUser.objects.get(pk=userID)
        userdata = UserProfile.objects.get(owner=user)
        userdata.bio = UserBio
        userdata.category = category
        userdata.socialmedia = json.dumps(social)
        userdata.config = json.dumps(config)
        userdata.save()
        proc = httpProc(request, None, None)
        return proc.ajax(1, None)
    except BaseException as msg:
        proc = httpProc(request, None, None)
        return proc.ajax(0, str("error:" + str(msg)))


def FetchProfileData(request, DataAjax):
    try:
        userID =  request.session['userID']
        user = BLUser.objects.get(pk=userID)
        userdata = UserProfile.objects.get(owner=user)
        data = {}
        data['FirstName'] = user.FirstName
        data['LastName'] = user.LastName
        data['email'] = user.email
        try:
            if (userdata.image == ""):
                data['Dpimage'] = "https://www.gravatar.com/avatar/" + hashlib.md5(user.email.lower().encode()).hexdigest() + "?"
            else:
                data['Dpimage'] = "http://127.0.0.1:8000/media/%s" % (userdata.image)
            data['bio'] = userdata.bio
            configdata = json.loads(userdata.config)
            data['phonenumber'] =configdata['userphone']
            data['companyname'] =configdata['companyname']
            data['website'] =configdata['userwebsite']
            data['category'] = userdata.category
            socialmedia = json.loads(userdata.socialmedia)
            data['Facebook'] = socialmedia['Facebook']
            data['Twitter'] = socialmedia['Twitter']
            data['Instagram'] = socialmedia['Instagram']
            data['Linkedin'] = socialmedia['Linkedin']
            data['Skype'] = socialmedia['Skype']
            data['Github'] = socialmedia['Github']
            proc = httpProc(request, None, None)
            return proc.ajax(1, data)
        except:
            pass
        proc = httpProc(request, None, None)
        return proc.ajax(1, data)
    except BaseException as msg:
        proc = httpProc(request, None, None)
        return proc.ajax(0, str("error:" + str(msg)))