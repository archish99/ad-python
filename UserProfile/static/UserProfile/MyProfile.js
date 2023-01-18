appmain.controller('userProfile', function ($scope, $http, $timeout) {
    $(document).ready(function () {
        $scope.FetchProfileData();
    });
    $scope.FetchProfileData = function () {
        url = "/Base/GlobalAjax";
        var maindata = {
            function: 'FetchProfileData'
        }
        var config = {
            headers: {
                'X-CSRFToken': getCookieMain('csrftoken')
            }
        };
        $http.post(url, maindata, config).then(OnSuccessProject, OnFail);

        function OnSuccessProject(res) {
            // console.log(res.data)
            var resp = res.data
            if (resp.status == 1) {
                console.log(resp.error_message.bio)
                $scope.DiplayBio = resp.error_message.bio
                $scope.Firstname = resp.error_message.FirstName
                $scope.LastName = resp.error_message.LastName
                $scope.useremail = resp.error_message.email
                $scope.userphone = resp.error_message.phonenumber
                $scope.category = resp.error_message.category
                $scope.companyname = resp.error_message.companyname
                $scope.userwebsite = resp.error_message.website
                $scope.FacebookURL = resp.error_message.Facebook
                $scope.TwitterURL = resp.error_message.Twitter
                $scope.InstagramURL = resp.error_message.Instagram
                $scope.LinkedinURL = resp.error_message.Linkedin
                $scope.SkypeURL = resp.error_message.Skype
                $scope.GithubURL = resp.error_message.Github
                $scope.Dpimage = resp.error_message.Dpimage
                console.log(resp.error_message);
            } else {
                alert(resp.error_message)
            }
        }

        function OnFail() {
            alert('Fail ')
        }

    }


    $scope.saveProfileData = function () {
        var userBio ;
        var firstname;
        var lastname;
        var userphone;
        var companyname;
        var userwebsite;
        var Facebook;
        var Twitter;
        var Instagram;
        var Linkedin;
        var Skype;
        var Github;
        if ($scope.Firstname == '' || $scope.Firstname == undefined) {
            alert("First Name is empty")
        } else {
            firstname = $scope.Firstname
        }
        if ($scope.LastName == '' || $scope.LastName == undefined) {
            alert("First Last is empty")
        } else {
            lastname = $scope.LastName
        }
        if ($scope.DiplayBio == '' || $scope.DiplayBio == undefined) {
            userBio = '-'
        } else {
            userBio = $scope.DiplayBio
        }
        if ($scope.userphone == '' || $scope.userphone == undefined) {
            userphone = '---- --- ---'
        } else {
            userphone = $scope.userphone
        }
        if ($scope.companyname == '' || $scope.companyname == undefined) {
            companyname = '------'
        } else {
            companyname = $scope.companyname
        }
        if ($scope.userwebsite == '' || $scope.userwebsite == undefined) {
            userwebsite = '-'
        } else {
            userwebsite = $scope.userwebsite
        }
        if ($scope.Facebook == '' || $scope.Facebook == undefined) {
            Facebook = 'facebook.com'
        } else {
            Facebook = $scope.Facebook
        }
        if ($scope.Twitter == '' || $scope.Twitter == undefined) {
            Twitter = 'twitter.com'
        } else {
            Twitter = $scope.Twitter
        }
        if ($scope.Instagram == '' || $scope.Instagram == undefined) {
            Instagram = 'instagram.com'
        } else {
            Instagram = $scope.Instagram
        }
        if ($scope.Linkedin == '' || $scope.Linkedin == undefined) {
            Linkedin = 'linkedin.com'
        } else {
            Linkedin = $scope.Linkedin
        }
        if ($scope.Skype == '' || $scope.Skype == undefined) {
            Skype = 'skype.com'
        } else {
            Skype = $scope.Skype
        }
        if ($scope.Github == '' || $scope.Github == undefined) {
            Github = 'github.com'
        } else {
            Github = $scope.Github

        }

        var dataa = {
            function: 'saveProfileData',
            userBio: userBio,
            firstname: firstname,
            lastname: lastname,
            userphone: userphone,
            companyname: companyname,
            userwebsite: userwebsite,
            Facebook: Facebook,
            Twitter: Twitter,
            Instagram: Instagram,
            Linkedin: Linkedin,
            Skype: Skype,
            Github: Github,
            category: $scope.category,
        }
        // console.log(dataa)
        GlobalAjaxMain(dataa, OnSuccessProject, OnFail)

        function OnSuccessProject(res) {
            if (res.status == 1) {
                alert('Done')
            } else {
                alert(res.error_message)
            }
        }

        function OnFail() {
            alert(('Fail '))
        }
    }
})
;