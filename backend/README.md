# MathFlex Back-end API

## Getting Started
Back end used pythons Flask HTTPs framework with SQLite database. All questions are stored within the SQLite databse mathflex.db. If Mathflex.db does not exist, it will be automatically created and populated with data.

### Prerequisits
Must have a valid python interpreter. Install the following libraries using `pip install <library>`:
- flask
- flask_cors
- datetime
- pytz
- PyJWT


### Entry Point
```python3 run.py``` - execute run.py with your python interpreter to run the back-end API.

## API REFERENCE

### Health Check
```http
  GET /api/health/status - Basic API health check
```


### Users Exist
```http
  GET /api/users/exists - Validate if a user exists.
```
*Request.body:*
| Parameter | Type     | Description                           |
| :-------- | :------- | :--------------------------------     |
| `email`   | `string` | **Required**. Email address of a user |


### Users Authentication
```http
  GET /api/users/auth - Authenticate a user with email and password.
```
*Request.body:*
| Parameter | Type     | Description                           |
| :-------- | :------- | :--------------------------------     |
| `email`   | `string` | **Required**. Email address of a user.|
| `password`| `string` | **Required**. Password of users.      |

### Users Create
```http
  GET /api/users/create - Create a user within database.
```
*Request.body:*
| Parameter | Type     | Description                           |
| :-------- | :------- | :--------------------------------     |
| `email`   | `string` | **Required**. Email address of a user.|
| `password`| `string` | **Required**. Password of user.       |

### Users Manage
```http
  GET /api/users/manage - Set active status to True/False for Unlock/Locking a user account.
```
*Request.headers:*
| Parameter        | Type      | Description                             |
| :--------        | :-------  | :--------------------------------       |
| `Autorization`   | `bearer`  | **Required**. Admin bearer token.       |
*Request.body:*
| Parameter | Type      | Description                             |
| :-------- | :-------  | :--------------------------------       |
| `email`   | `string`  | **Required**. Email address of a user.  |
| `active`  | `boolean` | **Required**. True=Unlock, False=Locked.|

### Users Remove
```http
  GET /api/users/manage - Set active status to True/False for Unlock/Locking a user account.
```
*Request.headers:*
| Parameter        | Type      | Description                             |
| :--------        | :-------  | :--------------------------------       |
| `Autorization`   | `bearer`  | **Required**. Admin bearer token.       |


*Request.body:*
| Parameter | Type      | Description                             |
| :-------- | :-------  | :--------------------------------       |
| `email`   | `string`  | **Required**. Email address of a user.  |

### Calls Questions
```http
  GET /api/calls/questions - Retrieve questions from database for user.
```
*Request.body:*
| Parameter   | Type       | Description                                         |
| :--------   | :-------   | :-------------------------------------------        |
| `email`     | `string`   | **Required**. Email address of a user.              |
| `limit`     | `integer`  | **Required**. Amount of questions to return, max=20.|
| `difficulty`| `integer`  | Grade difficulty level (1-8), defaults to random if not specified.|

```http
  POST /api/calls/questions - Insert question and user association in database.
```
*Request.body:*
| Parameter   | Type     | Description                                         |
| :--------   | :------- | :---------------------------------------------------|
| `email`     | `string` | **Required**. Email address of a user.              |
| `question`  | `string` | **Required**. Question user answered.               |
| `correct`   | `boolean`| **Required**. True/False if user answered correctly.|

