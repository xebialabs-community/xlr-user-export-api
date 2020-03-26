#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# Import common Python modules as needed
import os.path
import sys
import logging
import json
from datetime import datetime, timedelta

logging.basicConfig(filename='log/custom-api.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.debug("main: begin")

# PermissionApi
#     - List globalPermissions

# RoleApi
#     RoleView
#         - String name
#         - Set permissions
#         - Set<PrincipalView> principals

#     PrincipalView
#         - String fullname
#         - String username

# FolderApi
#     TeamView getTeams(folder.id)
#         - String id
#         - String teamName
#         - List<TeamMemberView> members
#         - List permissions

#     TeamMemberView
#         - String fullName
#         - String name
#         - MemberType type

#     MemberType
#         - PRINCIPAL
#         - ROLE

# UserApi
#     UserAccount
#         - String dateFormat
#         - String email
#         - Integer firstDayOfWeek
#         - String fullName
#         - Date lastActive
#         - String timeFormat
#         - String username
#         - boolean loginAllowed

# Process Users ----------------------
if 'userid' in request.query:
    logging.debug('has query parameter userid=%s' % request.query['userid'])
    user_obj_list = [userApi.getUser(request.query['userid'])]
else:
    logging.debug('get all users')
    page = None
    if 'page' in request.query:
        page = int(request.query['page'])

    resultsPerPage = None
    if 'resultsPerPage' in request.query:
        resultsPerPage = int(request.query['resultsPerPage'])

    # FYI: parameters are..  String email, String fullName, Boolean loginAllowed, Boolean external, Date lastActiveAfter, Date lastActiveBefore, Long page, Long resultsPerPage
    user_obj_list = userApi.findUsers(None, None, None, None, None, None, page, resultsPerPage)

users = {}
for user_obj in user_obj_list:
    user = {}
    user['fullName'] = user_obj.fullName
    user['email'] = user_obj.email
    user['loginAllowed'] = user_obj.loginAllowed
    user['lastActive'] = user_obj.lastActive
    user['roles'] = {}
    user['folders'] = {}
    users[user_obj.username] = user

# augment users with roles
roles = rolesApi.getRoles(0, 1000)

logging.debug('role processing...')
active_roles = []
for role in roles:
    if len(role.principals) > 0:
        logging.debug('  role %s' % role.name)

        r = {}
        r['name'] = role.name
        r['principals'] = []

        for principal in role.principals:
            username = principal.username.lower()
            logging.debug('    user %s in role %s' % (username, role.name))

            # the user query may be limited to a single user or a range of users
            # don't include the role if we have no principals for it
            if username in users:
                r['principals'].append(username)

                role_obj = {}
                role_obj['permissions'] = []
                for pem in role.permissions:
                    role_obj['permissions'].append(pem)

                users[username]['roles'][role.name] = role_obj

            else:
                logging.debug('  role principal not in user list')

        if len(r['principals']) > 0:
            active_roles.append(r)
        else:
            logging.debug('  role has no principals')

# Process Folders -------------------
rootFolders = folderApi.listRoot(0, 1000, 1, True)

def add_folder(user_folders, folder_obj, by_type):
    user_folders[folder_obj.title] = {}
    user_folders[folder_obj.title]['type'] = by_type
    user_folders[folder_obj.title]['permissions'] = team_obj.permissions

logging.debug('folder processing...')
for folder_obj in rootFolders:
    # get teams for the folder
    teams = folderApi.getTeams(folder_obj.id)

    # iterate over teams in this folder
    for team_obj in teams:
        # iterate over members in this team
        for member_obj in team_obj.members:
            logging.debug('  checking team member %s' % member_obj.name)

            # team members may be principals or roles
            # for roles, the team member name is the role
            if str(member_obj.type) == 'PRINCIPAL' and member_obj.name in users:
                # add folder to user
                add_folder(users[member_obj.name]['folders'], folder_obj, 'PRINCIPAL')

            elif str(member_obj.type) == 'ROLE':
                # check for users with this role
                for k in users:
                    user = users[k]
                    logging.debug('    checking user %s for role %s' % (user['fullName'], member_obj.name))
                    if member_obj.name in user['roles']:
                        # this user has role that matches the team member name, add folder
                        add_folder(user['folders'], folder_obj, 'ROLE')

# form response
response.statusCode = 200
response.entity = {
    "users": users,
    "roles": active_roles
}

logging.debug("main: end")
