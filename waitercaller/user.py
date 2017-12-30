class User:
    def __init__(self, email, salt, hash):
        self.email = email
        self.salt = salt
        self.hash = hash

    def get_id(self):
        return  self.email

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
