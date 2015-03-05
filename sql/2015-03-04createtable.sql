drop table IF EXISTS university_china;
CREATE TABLE university_china (
    id int(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(255),
    location VARCHAR(255),
    PRIMARY KEY(id)
);
drop TABLE IF EXISTS senior_high;
CREATE TABLE senior_high(
  id INT(11) NOT NULL AUTO_INCREMENT,
  name VARCHAR(255),
  provinice VARCHAR(255),
  city VARCHAR(255),
  dictrict VARCHAR(255),
  PRIMARY KEY(id)
);
drop TABLE IF EXISTS major_china;
CREATE TABLE major_china(
  id int(11) NOT NULL AUTO_INCREMENT,
  faculty_id int(11),
  faculty_name VARCHAR(255),
  major_id int(11),
  major_name VARCHAR(255),
  PRIMARY KEY(id)
)
