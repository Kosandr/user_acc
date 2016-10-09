'''
Added to UserPermissions:
   ###older new

   #TODO: optional decorator
   #decorator
   def requires_group(name):
      pass

   #resource access rights
   def perm_add_resource(res_name, groups, users):
      pass

   #def perm_modify_resource_rights(res_name):
   def perm_resource_add_group(name, group_name):
      pass
   def perm_resource_rm_group(name, group_name):
      pass
   def perm_resource_add_user(name, uname):
      pass
   def perm_resource_rm_user(name, uname):
      pass

   #decorator. Passes arg "allowed"
   def perm_resource_name(name):
      pass

   #TODO: optional
   #decorator
   def requires_group(name):
      pass

   ###old

   #this specific itemname can be accessed by this groups
   def add_granual_item(itemname, group_access_list):
      pass

   def check_user_check_granual_resource(itemname, uname):
      pass

   #possibly decorator
   def check_group(group_access):
      pass

   #same as above
   def requires_group(groups):
      pass

   #decorator for each resource, can give it name and it will be managed by granual_item
   def resource_perm(resourcename):
      pass

'''
