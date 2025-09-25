# A User Journey to develop with a sense of purpose

- [ ] register yourself as a new user (applicant)
- [ ] login as that user
- [ ] fill in one application form
- [ ] submit that application form
- [ ] view the submitted application form


## Relevant API Endpoints for this Journey

POST /users (create user)
POST /auth (login and receive a token, the token needs to be sent in the Authorization header for all subsequent requests)
POST /applications (create a new application form)
GET /applications/{id} (view a specific application form)


## User Creation Journey via Register Page

1. The Frontend appends the role "APPLICANT" because we can only register applicants via the register page.

2. Frontend creates a new user request by sending a POST request to the backend API endpoint `/users/` with user details as JSON payload.
This is what it should look like:

`user_create_payload`:

```json
{
  "username": "blabla",
  "role": "APPLICANT",
  "email": "user@example.com",
  "password": "mypassword"
}
```

We read this out and map it to a Pydantic model `UserCreate`, which we then use to create a new user model that holds a list of roles with one entry "APPLICANT"; also the password is hashed before storing it in the database.

Our defaults decide that the account will be active.

So we first have to create a new User object;
then we assign the role, timestamping that it was assigned now;
then we hash the password;
we collect all that and update the User object;
using SQLAlchemy, in a session we add the user to the DB and commit.
