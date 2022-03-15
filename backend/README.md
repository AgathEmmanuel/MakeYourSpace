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





CREATE TABLE accounts (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	created_on TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


TIMESTAMP WITH TIME ZONE

SELECT * FROM accounts;

DROP TABLE accounts;


INSERT INTO accounts(user_id,username,password,email)
VALUES (1,'username1','password1','email1')
RETURNING *;


DELETE FROM accounts WHERE id = 1;



psql -U postgres -d <database-name> -c "select * from accounts"
psql -U postgres -d <database-name> -c "INSERT INTO accounts(user_id,username,password,email) VALUES (1,'username1','password1','email1') RETURNING *;"



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
select * from accounts order by visitors DESC,user_id DESC;








```


https://www.postgresql.org/docs/9.1/sql-createtable.html  
https://www.tutorialspoint.com/postgresql/postgresql_create_table.htm  
https://www.postgresqltutorial.com/postgresql-create-table/  
https://www.postgresql.org/docs/9.3/ddl-default.html  
https://www.postgresql.org/docs/9.1/datatype-datetime.html  
https://www.postgresqltutorial.com/postgresql-drop-table/  
https://www.postgresqltutorial.com/postgresql-insert/  








