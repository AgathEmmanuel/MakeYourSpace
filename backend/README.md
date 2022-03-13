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

https://www.postgresql.org/docs/9.0/sql-createdatabase.html  


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

CREATE DATABASE name
    [ [ WITH ] [ OWNER [=] user_name ]
           [ TEMPLATE [=] template ]
           [ ENCODING [=] encoding ]
           [ LC_COLLATE [=] lc_collate ]
           [ LC_CTYPE [=] lc_ctype ]
           [ TABLESPACE [=] tablespace ]
           [ CONNECTION LIMIT [=] connlimit ] ]


```



