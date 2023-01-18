function GlobalAjax(data, SuccessCallBackack, FailureCallback) {
    $.ajax({
        url: "/Base/GlobalAjax",
        type: "POST",
        dataType: 'json', // type of response data
        timeout: 5000000,     // timeout milliseconds
        data: JSON.stringify(data),
        contentType: "application/json",
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: SuccessCallBackack,
        error: FailureCallback

    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var applicationlogin = angular.module('EscrowApplogin', []);


////



applicationlogin.controller('Login', function ($scope, $http, $window) {
    $scope.LoginUserEmailPasswd = function () {
        var data = {
            function: 'LoginUserEmailPasswd',
            email: $scope.email,
            password: $scope.password,
        }
        GlobalAjax(data, OnSuccessProject, OnFail)

        function OnSuccessProject(res) {
            if (res.status == 1) {
                $.toast('habbi'
                )
                $window.location.href = '/Base';


            } else {
                alert(res.error_message)
            }
        }

        function OnFail() {
            alert(('Fail '))
        }
    }
});


applicationlogin.controller('signuppagec', function ($scope, $http, $window) {
    // alert(";;;;;;;;;;;;;;;;;;;;")
    $scope.SingUpEmail = function () {
        var tremsandcondition = $scope.tremsandcondition;
        if (tremsandcondition == true) {
            var data = {
                function: 'SingUpEmail',
                Firstname: $scope.firstname,
                lastname: $scope.lastname,
                email: $scope.email,
                password: $scope.password,
            }
            GlobalAjax(data, OnSuccessProject, OnFail)

            function OnSuccessProject(res) {
                if (res.status == 1) {
                    $.toast('habbi'
                    )
                    $window.location.href = '/Login';


                } else {
                    alert(res.error_message)
                }
            }

            function OnFail() {
                alert(('Fail '))
            }

        } else {
            alert('Please accept Terms and Conditions')
        }

    }

    function handleCredentialResponse(response) {
        console.log("Encoded JWT ID token: " + response.credential);
        var data = {
            function: 'singupwith',
            WalletType: 'Google',
            Publicadress: response.credential
        }
        GlobalAjax(data, OnSuccessGoogleSU, OnFailGoogleSU)
    }

    window.onload = function () {
        google.accounts.id.initialize({
            client_id: "181170631609-j6v08sa4e3nfoolgb65r92lo3t2fgoc3.apps.googleusercontent.com",
            callback: handleCredentialResponse
        });
        google.accounts.id.renderButton(
            document.getElementById("buttonDiv"),
            {theme: "outline", size: "large"}  // customization attributes
        );
        google.accounts.id.prompt(); // also display the One Tap dialog
    }

    function OnSuccessGoogleSU(res) {
        if (res.status === 1) {
            $window.location.href = '/Base';
        } else {
            alert(res.error_message)
        }
        //
    }

    function OnFailGoogleSU(res) {
        alert(res.error_message)
        //
    }

    window.fbAsyncInit = function () {
        FB.init({
            appId: '583833066553737',
            cookie: true,
            xfbml: true,
            version: 'v14.0'
        });


        // FB.getLoginStatus(function (response) {   // Called after the JS SDK has been initialized.
        //     statusChangeCallback(response);        // Returns the login status.
        // }, {scope: 'public_profile,email'});
    };

    (function (d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) {
            return;
        }
        js = d.createElement(s);
        js.id = id;
        js.src = "https://connect.facebook.net/en_US/sdk.js";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

    $scope.SingUpFB = function () {
        FB.login(function (response) {
            statusChangeCallback(response);
        }, {scope: 'public_profile,email,ads_management,business_management,pages_manage_ads,manage_page', });
    }

    function statusChangeCallback(response) {  // Called with the results from FB.getLoginStatus().
        console.log('statusChangeCallback');
        console.log(response);                   // The current login status of the person.
        if (response.status === 'connected') {   // Logged into your webpage and Facebook.
            //testAPI();

            var data = {
                function: 'singupwith',
                WalletType: 'Facebook',
                Publicadress: response
            }
            GlobalAjax(data, OnSuccessGoogleSU, OnFailGoogleSU)
        } else {                                 // Not logged into your webpage or we are unable to tell.
            document.getElementById('status').innerHTML = 'Please log ' +
                'into this webpage.';
        }
    }

    function checkLoginState() {               // Called when a person is finished with the Login Button.
        FB.getLoginStatus(function (response) {   // See the onlogin handler
            statusChangeCallback(response);
        });
    }

});



