# eochat-backend 


This is REST-API made with DjangoRestFramework, which is part of a university project, designed for the Web Development course (INE5646 Programação para Web).

## Deployment

The api is currently deployed at  
https://protected-cove-50889.herokuapp.com/

## Signup

### Request

`POST /signup/`

    {username: 'new user', password: 'secret123'}

### Response

    HTTP 201 Created
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "username": "new user"
    }

## Login

### Request

`POST /token/`

    {username: 'new user', password: 'secret123'}

### Response

    HTTP 200 OK
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
    "token": "example4754bb904e2r2r"
    }

## NOTE: The next endpoints are authentication protected. You will need to pass the above token with the request header.
### Example with axios

    axios.get('/some-endpoint/', {headers: {Authorization: 'Token example4754bb904e2r2r'}})

## View logged in user information
### Request

`GET /me/`

    {}

### Response

    HTTP 200 OK
    Allow: GET, PUT, PATCH, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "username": "new user"
    }

## Edit logged in user information
Note that the patch method allows you to edit your information partially, only username, only password, or both, as demonstrated below:
### Request

`PATCH /me/`

    {username: 'new username'}
    {password: 'new password'}
    {username: 'new username', password: 'and new password'}

### Response

    HTTP 200 OK
    Allow: GET, PATCH, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "username": "new username"
    }

## Create a chat
### Request

`POST /chats/`

    {chat_name: 'new chat'}

### Response

    HTTP 201 Created
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "code": 625977,
        "name": "new chat",
        "created_at": "2021-12-08T17:54:32.949608-03:00"
    }

## Check if a chat exists
### Request

`GET /chats/<int:chat_code>/exists`

    {}

### Response

    HTTP 200 OK
    Allow: GET, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "exists": true
    }

## Join a chat
To join a chat, a websocket connection is required to
`ws://protected-cove-50889.herokuapp.com/ws/chat/<int:chat_code>`


