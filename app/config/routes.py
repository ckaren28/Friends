
from system.core.router import routes


routes['default_controller'] = 'Friends'
routes['/main'] = 'Friends#main'
routes['POST']['/create'] = 'Friends#create'
routes['POST']['/friends'] = 'Friends#login'
routes['/friends'] = 'Friends#home'
routes['/logout'] = "Friends#logout"
routes['POST']['/add/<friend_id>'] = "Friends#friending"
routes['/user/<user_id>'] = "Friends#view_profile"
routes['/remove/<user_id>'] = 'Friends#delete_friend'
