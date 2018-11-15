"""COntain User model."""
users = []


class User:
    """Class for user object."""

    user_id = 1

    def __init__(self, username=None, email=None, password=None):
        """Initialize User class."""
        self.username = username
        self.email = email
        self.password = password
        self.id = User.user_id

    def serialize_user(self):
        """Return tuple as user dictionary."""
        return dict(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password
        )

    def get_by_username(self, username):
        """Find a user by username."""
        for user in users:
            if user.username == username:
                return user

    def get_by_id(self, _id):
        """Find a user by id."""
        for user in users:
            if user.id == _id:
                return user
