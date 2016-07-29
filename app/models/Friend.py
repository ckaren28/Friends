""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re

class Friend(Model):
    def __init__(self):
        super(Friend, self).__init__()
    
    def create_user(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if not info['name']:
            errors.append('Name cannot be blank')
        elif len(info['name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not info['alias']:
            errors.append('Name cannot be blank')
        elif len(info['alias']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['pw_confirmation']:
            errors.append('Password and confirmation must match!')
        if errors:
            return {"status": False, "errors": errors}
        else:
            self.create_new_user(info)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            user = self.db.query_db(get_user_query)
            return {"status": True, "user":user[0] } 

    def create_new_user(self, info):
        password = info['password']
        hashed_pw = self.bcrypt.generate_password_hash(password)
        create_query = "INSERT INTO users(name, alias, email, pw_hash, birthday) VALUES (:name, :alias, :email, :pw_hash, :birthday)"
        create_data = {'name': info['name'], 'alias':info['alias'],'email':info['email'], 'pw_hash':hashed_pw, 'birthday':info['birthday']}
        self.db.query_db(create_query, create_data)

    def login_user(self, info):
        password = info['password']
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': info['email']}
        user = self.db.query_db(user_query, user_data)
        if user:
            
            if self.bcrypt.check_password_hash(user[0]['pw_hash'], password):
                return user[0]
            else:     
                return False
        else:
            return False

    def get_user_id(self, info):
        query = "SELECT * FROM users WHERE id = :user_id"
        data = {'user_id':info['user_id']}
        user= self.db.query_db(query, data)
        return user 

    def add_friend(self, user_id, friend_id):
        query = "INSERT INTO friends(user, user_friend) VALUES (:user, :user_friend)"
        data = {'user':user_id, 'user_friend':friend_id}
        return self.db.query_db(query, data)

    def my_friends(self, info):
        query = "SELECT * FROM friends LEFT JOIN users ON users.id = friends.user_friend WHERE user = :user_id"
        data = {'user_id':info['user_id']}
        return self.db.query_db(query, data)

    # def not_friends(self, info):
    #     query = "SELECT * FROM users LEFT JOIN friends ON friends.user = users.id WHERE user != :user_id "
    #     data = {'user_id':info['user_id']}
    #     return self.db.query_db(query, data)

    def all_people(self):
        return self.db.query_db("SELECT * FROM users")

    def delete_friend(self, user_id):
        query = "DELETE FROM friends WHERE user_friend = :user_id"
        data = {'user_id': user_id}
        return self.db.query_db(query, data)













