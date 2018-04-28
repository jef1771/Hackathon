-- noinspection SqlNoDataSourceInspectionForFile

DROP TABLE IF EXISTS users;

CREATE TABLE users (

  id INTEGER PRIMARY KEY autoincrement,

  email text NOT NULL,

  username text NOT NULL,

  password text NULL,

  skills text NULL,

  int text NULL

);