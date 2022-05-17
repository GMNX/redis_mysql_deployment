create database myapp_database;
use myapp_database;

CREATE TABLE myapp_table
(
id INTEGER AUTO_INCREMENT,
redis_key TEXT,
value TEXT,
PRIMARY KEY (id)
);