**Get User**
----
  Returns JSON data about a single user.

* **URL**

  /users/:username/:password

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `username=[string]`
   `password=[string]`
   

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `{ user : {
                        name: "John",
                        surname: "Doe",
                        type: "teacher",
                        username:"admin",
                        password:"hashed_password""}
                  }`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "Not found }`

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ error : "Bad request" }`