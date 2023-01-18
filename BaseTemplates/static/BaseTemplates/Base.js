var appmain = angular.module("EscrowAppMain", []);

appmain.config([
  "$interpolateProvider",
  function ($interpolateProvider) {
    $interpolateProvider.startSymbol("{$");
    $interpolateProvider.endSymbol("$}");
  },
]);
function GlobalAjaxMain(data, SuccessCallBackack, FailureCallback) {
  $.ajax({
    url: "/Base/GlobalAjax",
    type: "POST",
    dataType: "json", // type of response data
    timeout: 5000000, // timeout milliseconds
    data: JSON.stringify(data),
    contentType: "application/json",
    headers: {
      "X-CSRFToken": getCookieMain("csrftoken"),
    },
    success: SuccessCallBackack,
    error: FailureCallback,
  });
}

function getCookieMain(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function Logout() {
  var data = {
    function: "Logout",
  };
  GlobalAjaxMain(data, OnSuccessProject, OnFail);

  function OnSuccessProject(res) {
    if (res.status == 1) {
      location.reload();
    } else {
      alert(res.error_message);
    }
  }

  function OnFail() {
    alert("Fail ");
  }
}

appmain.controller("GoogleAds", function ($scope, $http, $timeout) {
  // $(document).ready(function () {
  //     $scope.FetchProfileData();
  // });
  $scope.GoogleAdsAuth = function () {
    url = "/Base/GlobalAjax";
    var maindata = {
      function: "GoogleAuthRedirect",
    };
    var config = {
      headers: {
        "X-CSRFToken": getCookieMain("csrftoken"),
      },
    };
    $http.post(url, maindata, config).then(OnSuccessProject, OnFail);

    function OnSuccessProject(res) {
      // console.log(res.data)
      var resp = res.data;
      console.log("res:: ", res.data);
      if (resp.status == 1) {
        console.log(resp.error_message.bio);
        window.location.href = resp.error_message;
      } else {
        alert(resp.error_message);
      }
    }

    function OnFail() {
      alert("Fail ");
    }
  };
});
