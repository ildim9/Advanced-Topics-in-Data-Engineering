create database if not exists assignment_impala;

use assignment_impala ;
################ 3a) Creation of the Tables

 CREATE TABLE `Student` (
 `sid` int NOT NULL,
 `name` varchar(50) NOT NULL,
  PRIMARY KEY (`sid`) 
 );

CREATE TABLE `course` (
  `cid` int NOT NULL,
  `title` varchar(50) NOT NULL,
  `description` TEXT NOT NULL,
  PRIMARY KEY (`cid`) 
  );

CREATE TABLE `attended` (
  `ac_year` char(9) NOT NULL,
  `grade` NUMERIC(1) NOT NULL,
  `sid` int NOT NULL,
  `cid` int NOT NULL,
  key `sid_index` (`sid`),
  key `cid_index` (`cid`),
  constraint `cid` foreign key (`cid`) references `course` (`cid`),
  constraint `sid` foreign key  (`sid`) references `student` (`sid`)
  );

 ##### 3b) Insertion of data to students table 
INSERT INTO student
 VALUES 
(102,'Ilias');


######	3c) Write a statement that retrieves all the names of the students 
######          that have attended the course having title “Artificial Intelligence” 
######			during the academic year “2021-2022”.

#### In order to validate our queries we will fill the tables with random 
#### entries

INSERT INTO student
VALUES 
(103,'Tzeni'),
(104,'Pantelis'),
(105,'Teo'),
(106,'Chrysa'),
(107,'Katerina'),
(108,'Giannis');

INSERT INTO course
VALUES 
(1,'Artificial Intelligence','main'),
(2,'Data Analysis','sub'),
(3,'Business Process Management','main'),
(4,'Large Scale Optimazation','main'),
(5,'Statistics for Business Analytics','main');

INSERT INTO attended VALUES 
("2021-2022",8,102,2),
("2021-2022",3,102,1),
("2021-2022",9,103,1),
("2022-2023",6,107,1),
("2018-2019",4,108,4),
("2019-2020",5,104,3),
("2017-2017",4,105,3),
("2019-2020",3,107,4);

select  name 
from student
join attended
on student.sid = attended.sid 
join course 
on attended.cid = course.cid 
where course.title ='Artificial Intelligence' and attended.ac_year in ("2021-2022") ;

######   3d) Write a statement that retrieves the titles and the average grades of all the courses for
######       which the average grade of the students that attended them is lower than 6

select title, round(avg(grade),1) as average_grade  
from course
join attended 
on attended.cid = course.cid
group by title
having average_grade < 6;








