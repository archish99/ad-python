function GlobalAjax(data,  SuccessCallBackack, FailureCallback){
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

var app = angular.module('EscrowApp', []);