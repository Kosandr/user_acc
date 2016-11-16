import json

#api.py API errors
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
   2 = req_type doesn't have a vaid resource name. Look in get_res_name_from_req_type()
   3 = bad return type for permission from acc_mgr.get_resource_user_perms()
   4 = handle_get__x permission denied
   5 = handle_get__user_groups bad uname (for some reason it's None)
   6 = handle_get__user_groups.get_user_groups bad return
   7 = handle_get__group_members bad group_name (it's None)
   8 = handle_get__group_members.get_group_members acc_mgr.get_group_members() failed
   ###bad### 9 = post isn't supported
   10 = request type isn't supported (only GET/POST)
   11 = submit form err. extra is a string empty_data/not_str/bad_json
   12 = request 'type' is unknown
   13 = failed login
      extra: 1 = username doesn't exist, 2 = bad uname internal error, 3 = bad pass, 4 = other, 0 = success {no 0 BAD DOESNT EXIST TODO}
      extra userside js error: 13 = either empty username or pass
   14 = failed registration
      extra userside js error:
         100 = passwords don't match
      extra:
         7 = uname too short
         8 = pass to short
         9 = username taken (credentials sys)
         10 = uname or pass none
         11 = username taken (permission sys)
         22 = userperm user exists (ac.new_user() as opposed to ac.user_exists())
         23 = userperm uname too short (min 4 chars)
         31 = secpassdb username taken
         32 = bad username (too short)
         33 = bad password (too short)
   15 = onFail of jquery.ajax. Only used in javascript and doesnt touch python
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


#Errors for userpage.py
#0 = unknown
#1-3 bad data passed in POST for login() page
#1 = form is None
#2 = no 'type' in form
#3 = form 'type' is uknown
#4 = register no uname
#5 = register no email
#6 = register no password
#7 = register username too short
#8 = register pass too short
#9 = register account_exists (cred storage)
#10 = !!! NOT IMPLEMENTED register group exists (cred storage). only needed if each user must have his own group
#11 = register user_exists() (permission system)
#12 = (12, 'perm_err', ret_code) = register ac.new_user() failed
#13 = (13, 'cred_err', ret_code) = register ac.add_account() failed
#14 = login no uname
#15 = login no password
def internal_error(code=0, msg=''):
   return 'error (code: %s) (msg: %s)' % (code, msg)


