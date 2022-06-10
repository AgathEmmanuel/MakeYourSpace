# Backend






## steps  

```
virtualenv envMakeYourSpace
source envMakeYourSpace/bin/activate


pip install "fastapi[all]"


# to start uvicorn server

cd backend

uvicorn main:app             #if the file name is main.py

uvicorn main:app --reload    #if the file name is main.py

vicorn app.main:app --reload 	# if file is in app directory  

```


# Database  

DBMS( Database Management System ) will be used to interact with database  

Postgresql  

default port 5432  



### Setting up a PostgreSQL database using Docker  

```

docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres  

this will open the port to the local  
you can use programs like DBeaver to connect to database  
The default postgres user and database are created in the entrypoint with initdb  


docker exec -it NAME_OF_CONTAINER psql -U YOUR_POSTGRES_USERNAME  



```

### psql commands  


```

psql -d database -U user -W	Connects to a database under a specific user	
				-d: used to state the database name 
				-U:used to state the database user


\c dbname	Switch connection to a new database	 
\l		List available databases	 
\dt		List available tables	 
\d table_name	Describe a table such as a column, type, modifiers of columns, etc.	 
\dn		List all schemes of the currently connected database	 
\df		List available functions in the current database	 
\dv		List available views in the current database	 
\du	 	List all users and their assign roles	 
\g		Execute the last command again	 
\s		Display command history	 
\s filename	Save the command history to a file	 
\i filename	Execute psql commands from a file	 
\?		Know all available psql commands	 
\h		Get help
\e		Edit command in your own editor	 
\a		Switch from aligned to non-aligned column output	 
\H		Switch the output to HTML format	 
\q		Exit psql shell

SELECT version();	Retrieve the current version of PostgreSQL server	 


CREATE DATABASE test1;
CREATE DATABASE test1 OWNER test1owner TABLESPACE test1space;



```

https://www.postgresql.org/docs/9.0/sql-createdatabase.html  
https://www.postgresql.org/docs/9.5/datatype.html  



### Dtabase Table schema definitions  

> sample examples

```

CREATE TABLE accounts (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	created_on TIMESTAMP NOT NULL,
        last_login TIMESTAMP 
);



CREATE TABLE roles(
   role_id serial PRIMARY KEY,
   role_name VARCHAR (255) UNIQUE NOT NULL
);


CREATE TABLE account_roles (
  user_id INT NOT NULL,
  role_id INT NOT NULL,
  grant_date TIMESTAMP,
  PRIMARY KEY (user_id, role_id),
  FOREIGN KEY (role_id)
      REFERENCES roles (role_id),
  FOREIGN KEY (user_id)
      REFERENCES accounts (user_id)
);


TIMESTAMP WITH TIME ZONE



```

> MakeYourSpace tables

```

CREATE DATABASE makeyourspace;


CREATE TABLE accounts (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	created_on TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);



DROP TABLE accounts;


SELECT * FROM accounts;
INSERT INTO accounts(user_id,username,password,email)
VALUES (1,'username1','password1','email1')
RETURNING *;


DELETE FROM accounts WHERE id = 1;



psql -U postgres -d <database-name> -c "select * from accounts"
psql -U postgres -d <database-name> -c "INSERT INTO accounts(user_id,username,password,email) VALUES (1,'username1','password1','email1') RETURNING *;"


to populate the database with random data use INSERT+SELECT

for i in {1..9};do docker exec -it <image-id>  psql -d <database-name> -U postgres -c "select * from accounts";done;

for i in {1..9};do docker exec -it <image-id>  psql -d <database-name> -U postgres -c "INSERT INTO accounts(user_id,username,password,email) VALUES ($i,'username$i','password$i','email$i') RETURNING *;";done;


select user_id,password from accounts;
select user_id as id,password as pwd from accounts;
select user_id,password from accounts where user_id = 8;
select user_id,password from accounts where user_id > 3;
select user_id,password from accounts where user_id in (1,2,3);
select * from accounts where email like 'ema%';
select * from accounts where email like '%es%';
select * from accounts where email not like '%es%';


ALTER TABLE accounts
ADD COLUMN visitors int;

UPDATE accounts SET visitors=999 WHERE user_id = 1;

for i in {1..13};do docker exec -it <image-id> psql -d <database-name> -U postgres -c "UPDATE accounts SET visitors=$(($RANDOM)) WHERE id = $i;";done;


to populate the database with random data use INSERT+SELECT


select * from accounts order by visitors;
select * from accounts order by visitors ASC;
select * from accounts order by visitors DESC;
select * from accounts order by visitors DESC,user_id;
select * from accounts order by visitors DESC,user_id DESC;
select * from accounts order by visitors WHERE user_id=1 or user_id=2 or user_id=3  
select * from accounts LIMIT 10; 
select * from accounts WHERE user_id>10 LIMIT 2;
select * from accounts ORDER BY user_id LIMIT 15 OFFSET 5;

UPDATE accounts SET password='1234' WHERE user_id=2;


create table posts ( 
	user_id serial PRIMARY KEY, 
	title VARCHAR NOT NULL, 
	content VARCHAR, 
	description VARCHAR, 
	post_status BOOLEAN NOT NULL DEFAULT TRUE, 
	creation_time TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);



INSERT INTO posts(user_id,title)
VALUES (1,'This is a pleasant day')
RETURNING *;

```


https://www.postgresql.org/docs/9.1/sql-createtable.html  
https://www.tutorialspoint.com/postgresql/postgresql_create_table.htm  
https://www.postgresqltutorial.com/postgresql-create-table/  
https://www.postgresql.org/docs/9.3/ddl-default.html  
https://www.postgresql.org/docs/9.1/datatype-datetime.html  
https://www.postgresqltutorial.com/postgresql-drop-table/  
https://www.postgresqltutorial.com/postgresql-insert/  


### Postgress driver  

https://www.psycopg.org/docs/  

> Psycopg :  

PostgreSQL database adapter for the Python programming language

> features : 

implementation of the Python DB API 2.0 specification  
thread safety (several threads can share the same connection)  
designed for heavily multi-threaded applications  
create and destroy lots of cursors  
make a large number of concurrent INSERTs or UPDATEs  
client-side and server-side cursors, asynchronous communication and notifications, COPY support 
many Python types are supported out-of-the-box and adapted to matching PostgreSQL data types 
flexible objects adaptation system allows adpatation to be extended and customized 



```

------- db_credential.py-----------
db_database = "examplename"
db_user = "exampleusername"
db_password = "examplepassword"
-----------------------------------

```

### ORM (Object Relational Mapper)  

Sqlalchemy  
Alembic  

https://www.sqlalchemy.org/  
https://fastapi.tiangolo.com/tutorial/sql-databases/  


Schema/Pydantic Models  

defines the structure of request and response  
request will only go through only if it has a proper structure  

Sqlalchemy Models  

defines the columns of the table in database  
perform CRUD operations on database  



### JWT Authentication  

- session based authentication  
we store something on our backend server to track weather a user is logged in  
this can be stored in memory  or  database  

- jwt authentication  
stateless, here there is nothing in the backend for tracking user if he is logged in or out  
the token is stored in the frontend  client to keep track  

1. client sents username + password to api  
2. if credentials are valid server signs JWT token  
3. server sents response back with token  
4. client can now start using resources that require authentication  
5. client will sent the token along with the requests to the server  
6. server at the api end point  will verify the that the token is valid  
7. if the token is valid server will send back the requested data  

jwt token is not encrypted  
token is made up of 3 individual pieces  

HEADER:  
includes metadata about the token  
alg = algorithm that is used for signing  
typ = JWT  

PAYLOAD:  
is not encrypted  
so its not good to pass any confidential information in it  
common things that can be put in the payload  
id of user  
role of user  
etc  
including a lot of info in the token can increase the size of packet  
and result in lose of some bandwidth  

SIGNATURE:  
combination of 3 things-  
HEADER + PAYLOAD + Secret  
Secret is a special password that we keep in the api  
we pass this 3 information and pass it into the signing algorithm  
and it will return a signature  

even if a hacker try to tweek the payload with different admin privileger  
or user ids the signature will not match with his new payload and since  
he does not have secret cant generate updated signature  

the server can verify if the token is valid by doing a simple task  
of taking the header, payload and secret to create a new signature  
and comparting it with the signature that came in with the request  


> User Log in  
1. user send login info with email and password to the endpoint  
2. server finds user by email or username from the database  
3. database gives back the user infor and the hashed password  
4. server hashes the pasword from user and compares it with hashed passwork from database  



https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/  
jwt.io  






### Redis  

- stands for Remote Dictionary Server, is a fast, open source, in-memory, key-value data store.  
- used as a database, cache, message broker, queue , for caching, session management, gaming, leaderboards, real-time analytics, geospatial, ride-hailing, chat/messaging, media streaming, and pub/sub apps. 
- delivers sub-millisecond response times, enabling millions of requests per second for real-time applications in industries like gaming, ad-tech, financial services, healthcare, and IoT  
- redisjson database is similar to mongodb and can be used for storing data  
- redisstreams can be used for senting events from one microservice to another  
 

you can post your works for a prize  
all your posts will be visible in the general home page at frontend for all users  
user can come and buy them via a payment service  


the posts are stored in the postgress database service  
once your work is bought by a user it will create an event and update your post as sold  
we make use of asynchronous communication in backgroud to do the updation

the currency service (written in go will be available) to match the price with different countries



# Links  

[https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)  
[https://developer.mozilla.org/en-US/docs/Web/HTTP/Status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)  
[https://blog.logrocket.com/building-a-graphql-server-with-fastapi/](https://blog.logrocket.com/building-a-graphql-server-with-fastapi/)    
[https://redis.com/blog/5-industry-use-cases-for-redis-developers/](https://redis.com/blog/5-industry-use-cases-for-redis-developers/)  
[https://www.redis.io/docs/manual/data-types/streams/](https://www.redis.io/docs/manual/data-types/streams/)  
[https://goswagger.io/](https://goswagger.io/)  
