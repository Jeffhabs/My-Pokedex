# f16-authentication-Jeffhabs
# Authentication for Pokedex
#### Resources
  * /users
  * /sessions
  * /pokemon

#### Attributes
  * Users:
    * id
    * first name
    * last name
    * (encrypted)password
    * email
  * Pokemon:
    * id
    * name
    * gender
    * type
    * size
    * strength
    * weakness

#### Database Schema
    CREATE TABLE users (
      id INTEGER PRIMARY KEY,
      name VARCHAR(64),
      f_name VARCHAR(64),
      l_name VARCHAR(64),
      password VARCHAR(64),
      email VARCHAR(64)
      );

    CREATE TABLE pokemon (
      id INTEGER PRIMARY KEY,
      name VARCHAR(64),
      gender VARCHAR(64),
      type VARCHAR(64),
      size VARCHAR(64),
      strength VARCHAR(64),
      weakness VARCHAR(64)
      );
#### REST Endpoints for Pokemon
HTTP Method | CRUD | Entire Collection (e.g. /pokemon) | Specific Item (e.g. /pokemon/{id})
----------- | ---- | --------------------------------- | ---------------------------------
POST | Create | 201 (created) no body response text | 404 (Not Found) Already exists
GET | Read | 200 (OK), list of all pokemon | 200 (OK) single pokemon 404 (Not Found)
PUT | Update | 404 (Not Found) does not update entire collection | 204 (No content) 404 (Not Found) id not found/invalid
DELETE | Delete | 404 (Not Found) does not delete entire collection | 200 (OK) 404 (Not Found) if id not found/invalid

#### REST Endpoints for Users
HTTP Method | CRUD | Entire Collection (e.g. /users)
----------- | ---- | ---------------------------------
POST | Create | 201 (created) no body response text, 401 (unauthorized) |

#### REST Endpoints for Sessions
HTTP Method | CRUD | Entire Collection (e.g. /sessions)
----------- | ---- | ---------------------------------
POST | Create | 201 (created) user body response text, 401 (unauthorized) |

#### Sample JSON Pokemon
    [
      .....
      {
       "id": 44,
       "name": "Ponyta",
       "gender": "Female",
       "type": "Fire",
       "size": "Large",
       "strength": "Grass",
       "weakness": "Water"
      },
      .....
    ]

#### Sample JSON Users
    {
      "f_name": "Han",
      "l_name": "Solo",
      "email": nerfherder55@example.com
    }
