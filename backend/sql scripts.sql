-- CREATE DATABASE `FinalProject` ;


#### AIRPORTS ####
-- SELECT * FROM airports
-- Create table airports 
CREATE TABLE IF NOT EXISTS airports(
id int AUTO_INCREMENT PRIMARY KEY,
airportcode VARCHAR(100) NOT NULL,
airportname VARCHAR(100) NOT NULL,
country VARCHAR(100) NOT NULL
);


#### PLANES ####
-- SELECT * FROM planes
-- Create table planes 
CREATE TABLE IF NOT EXISTS planes(
id int AUTO_INCREMENT PRIMARY KEY,
make VARCHAR(100) NOT NULL,
model VARCHAR(100) NOT NULL,
year int(4) NOT NULL,
capacity int(15) NOT NULL
);


-- #### FLIGHTS ####
-- SELECT * FROM flights
-- Create table flights 
-- learned foreign key through: https://www.w3schools.com/mysql/mysql_foreignkey.asp
CREATE TABLE IF NOT EXISTS flights(
id int AUTO_INCREMENT PRIMARY KEY,
planeid int NOT NULL,
airportfromid int NOT NULL,
airporttoid int NOT NULL,
date date NOT NULL,
FOREIGN KEY (planeid) REFERENCES planes(id),
FOREIGN KEY (airportfromid) REFERENCES airports(id),
FOREIGN KEY (airporttoid) REFERENCES airports(id)
);
