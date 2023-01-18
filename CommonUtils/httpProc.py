# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse
import json

class httpProc:
    def __init__(self, request, templateName, data = None, function = None):
        self.request = request
        self.templateName = templateName
        self.data = data
        self.function = function


    def render(self):
        try:
            try:
                resp = render(self.request, self.templateName, self.data)
                #resp['Referrer-Policy'] = 'strict-origin-when-cross-origin'
                return resp

            except BaseException as msg:
                templateName = 'baseTemplate/error.html'
                return render(self.request, templateName, {'error_message': str(msg)})
        except BaseException as msg:
            print("rander error...........:"+str(msg))


    def renderPre(self):
        if self.data == None:
            return render(self.request, self.templateName)
        else:
            return render(self.request, self.templateName, self.data)

    def ajaxPre(self, status, errorMessage, success = None):
        final_dic = {'status': status, 'error_message': errorMessage, 'success': success}
        final_json = json.dumps(final_dic)
        return HttpResponse(final_json)

    def ajax(self, status, errorMessage, data = None):
        if data == None:
            finalDic = {'status': status, 'error_message': errorMessage}
            finalJson = json.dumps(finalDic)
            return HttpResponse(finalJson)
        else:
            finalDic = {}
            finalDic['status'] = status
            finalDic['error_message'] = errorMessage

            for key, value in data.items():
                finalDic[key] = value

            finalJson = json.dumps(finalDic)
            return HttpResponse(finalJson)

    @staticmethod
    def AJAX(status, errorMessage, success = None):
        final_dic = {'status': status, 'error_message': errorMessage, 'success': success}
        final_json = json.dumps(final_dic)
        return HttpResponse(final_json)




