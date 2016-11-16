import json

'''TODO permissions
req.args = {
     'type':     'user_list'/'user_groups'/'all_groups'
}
if (req.type == 'user_groups') //mandatory arguments
   req['uname'] = string
   //# req['per_page'] = None/int
   //# req['page_n'] = None/int

/////response
res = {
     'success': true/false,
     'err' : None/{ 'code' : int, 'method' : func/None, 'extra' : extra_dict/None},
     'extra' : None/extraData,
}

if (req.type == 'user_list')
   res['ret']['users'] = ['uname', 'uname', 'uname']
if (req.type == 'user_groups')
   current:
      res = { 'uname' : xx, 'groups' : ['group1', 'group2', 'etc..'] }
   todo:
      res['extra'] = { 'uname' : xx, 'groups' : ['group1', 'group2', 'etc..'] }

err = res['err']
err['code']
   0 = unknown
   1 = Missing request type or it isn't string. Invalid request
'''
def mk_err(code, method, extra=None):
   return {
      'code' : code,
      'method' : method,
      'extra' : extra
   }
def ret_fail(resp, code, method, extra=None):
   resp['success'] = False
   resp['err'] = mk_err(code, method, extra)
   return json.dumps(resp)
def ret_success(resp, data=None):
   resp['success'] = True
   resp['extra'] = data
   return json.dumps(resp)


#SurveyDb err
#err: {'code':int, 'desc':str})
#codes = [
#     (0, desc) = json_data not dict
#     (1, section_name) = section "section_name" missing from json
#     (2, section_name) = section "section_name" isn't a dict
#     (3, {'ccode':x, 'index':-1}) = bad liability. index starts at 0
#     (4, {'ccode':x, 'index':-1}) = bad asset. index starts at 0

#           ccode 10 = assets/liabs Info not list
#           ccode 11 = asset/liab with index 'index' is not dict
#           index -1 = not in index
def mkerr(code, desc=None):
   return Maybe(desc, code) #(False, {'code':code, 'desc':desc})
def iserr(ret):
   return ret.is_err()
   #return ret[0] != -1

