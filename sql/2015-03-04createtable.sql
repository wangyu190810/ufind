CREATE TABLE university_china(
    id INTEGER NOT NULL DEFAULT AUTHORIZATION ,
    name VARCHAR(255),
    location VARCHAR (255),
    PRIMARY KEY (id)
)

CREATE TABLE senior_high(
  id INTEGER NOT NULL DEFAULT AUTHORIZATION ,
  name VARCHAR (255),
  location VARCHAR (255),
  provinice VARCHAR (255),
  city VARCHAR (255),
  dictrict VARCHAR (255),
  PRIMARY KEY (id)
)

CREATE TABLE major_china(
  id INTEGER NOT NULL DEFAULT AUTHORIZATION ,
  faculty_id INTEGER ,
  faculty_name VARCHAR (255)
  major_id INTEGER ,
  major_name VARCHAR (255),
  PRIMARY KEY (id)
)