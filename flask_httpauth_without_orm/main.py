from json import load
from typing import Dict, Optional

from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

auth = HTTPBasicAuth()

users: Dict[str, "User"] = {}


class User:
    def __init__(self, id: str, username: str, email: str, password: str):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def get(username: str) -> Optional["User"]:
        return users.get(username)

    def __str__(self) -> str:
        return f"<Id: {self.id}, Username: {self.username}, Email: {self.email}>"

    def __repr__(self) -> str:
        return self.__str__()


with open("users.json") as file:
    data = load(file)
    for key in data:
        users[data[key]["username"]] = User(
            id=key,
            username=data[key]["username"],
            email=data[key]["email"],
            password=data[key]["password"],
        )


@auth.verify_password
def verify_password(username: str, password: str):
    user = User.get(username)
    if user and user.password == password:
        return username


@app.get("/")
@auth.login_required
def index():
    username = auth.current_user()
    return f"""
        <h1>Hi {username}</h1>
        <h3>Welcome to Flask HTTPAuth without ORM!</h3>
    """
