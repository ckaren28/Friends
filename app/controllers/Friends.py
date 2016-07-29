"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Friends(Controller):
    def __init__(self, action):
        super(Friends, self).__init__(action)
      
        self.load_model('Friend')
        self.db = self._app.db

       
   
    def index(self):
        return redirect('/main')

    def main(self):
        return self.load_view('index.html')

    def create(self):
        user_info = {
            'name': request.form['name'],
            'alias': request.form['alias'],
            'email': request.form['email'],
            'password': request.form['password'],
            'pw_confirmation': request.form['confirmpw'],
            'birthday':request.form['birthday']
            }
        create_status = self.models['Friend'].create_user(user_info)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['alias'] = create_status['user']['alias']
            alias = session['alias']
            return redirect('/friends')
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/')

    def login(self):
        user_info={
            'email': request.form['email'],
            'password': request.form['password']
        }
        user = self.models['Friend'].login_user(user_info)

        if user == False:
            flash('wrong.')
            return redirect('/')
        else:
            session['alias'] = user['alias']
            session['id'] = user['id']
            alias = user['alias']
            return redirect('/friends')

    def logout(self):
        session.clear()
        return redirect('/')

    def home(self):
        info = {'user_id':session['id']}
        my_friends = self.models['Friend'].my_friends(info)
        # not_friends = self.models['Friend'].not_friends(info)
        all_users = self.models['Friend'].all_people()
        display_friends = []
        for person in all_users:
            is_a_fav = False
            for friend in my_friends:
                if friend['user_friend'] == person['id']:
                    is_a_fav = True
            if is_a_fav == False:
                display_friends.append(person)
        return self.load_view('home.html', alias= session['alias'], my_friends = my_friends, all_users = all_users, display_friends = display_friends)

    def view_profile(self, user_id):
        user_info ={'user_id':user_id}
        user = self.models['Friend'].get_user_id(user_info)
        return self.load_view('friend_profile.html', user = user )

    def friending(self, friend_id):
        add_friend = self.models['Friend'].add_friend(session['id'], friend_id)
        return redirect('/friends')

    def delete_friend(self, user_id):
        deleting = self.models['Friend'].delete_friend(user_id)
        return redirect('/friends')










