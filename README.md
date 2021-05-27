# Backend_redart
 Backend for the Redart
This is the backend with simple functionality written with FastAPI and PostgreSQL

There are 3 classes of users
Users, Artists, Admin

Users:
can access Filters
create, update, delete personal information

Artists:
extends the functionality of Users. They can upload Filters and give title and description to it, however it should pass a approval of Admin before Filters can be accessed by Users. 

Admins:
Can CRUD Users, Artists and Filters
