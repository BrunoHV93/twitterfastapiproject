# Python
import json # Para trabajar con archivos json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Path

app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id: UUID =  Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )    

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(...,
    min_length=1,
    max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)


# Path Operations

## Users

### Register a user

@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["Users"]
)
def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path operation register a user in the app

    Parameters:
        -Request body parameter
            -user: UserRegister
    
    Returns a json with the basic user information:
        - user_id: UUID
        - email: EmailSt
        - first_name: str
        - last_name: str
        - birth_date: str
    """
    # Tenemos los usuarios a cargar en un archivo (normalmente, no es así, provienen de base de datos), leemos archivo y
    # metemos resultado en una variable, pero como queremos manejar jsons metemos json.loads
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        # Para moverse a inicio del archivo, se pone cero para ir a bite cero
        f.seek(0)
        f.write(json.dumps(results))
        return user


### Login a user

@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login():
    pass

### Show all users

@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    Show all users

    This path opetarion show all users in the app

    Parameters:
        -

    Retursn a json list with all users in the app, with the following keys:
        - user_id: UUID
        - email: EmailSt
        - first_name: str
        - last_name: str
        - birth_date: str
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        print(results)
        return results

### Show a user

@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a users",
    tags=["Users"]
)
def show_a_user(
    user_id: int = Path(
        ...,
        ge=0,
        title="User ID",
        description="This is the User ID"
    )
    ):
    """
    Show a user

    This path opetarion show an specific user in the app

    Parameters:
        -

    Retursn a json list with all users in the app, with the following keys:
        - user_id: UUID
        - email: EmailSt
        - first_name: str
        - last_name: str
        - birth_date: str
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        if user_id >= len(results):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This User doesn´t exist"
            )
        return results[user_id]

### Delete a user

@app.delete(
    path="/users/{users_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user():
    pass

### Update a user

@app.put(
    path="/users/{users_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user():
    pass


## Tweets

### Show all tweets

@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
def home():
    pass

### Post a tweet

@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
    Post  tweet

    This path operation post a tweet in the app

    Parameters:
        -Request body parameter
            -tweet: Tweet
    
    Returns a json with the basic tweet information:
        - tweet_id: UUID
        - content: str
        - created_at: datetime 
        - updated_at: Optional[datetime]
        - by: User
        """

    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])

        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

### Show a tweet

@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet():
    pass

### Delete a tweet

@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet():
    pass

### Update a tweet

@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet():
    pass