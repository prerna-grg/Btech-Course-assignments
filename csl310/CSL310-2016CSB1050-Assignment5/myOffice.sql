drop database if exists myOffice;
create database myOffice;

USE myOffice;


create table Contact_information(
	ID int NOT NULL auto_increment,
	StreetAddress varchar(40),
	City varchar(20),
	State varchar(20),
	Country varchar(20),
	PostalCode varchar(10),
	Phone varchar(20),
	Mobile varchar(20),
	Email varchar(30),
	primary key(ID));
	

create table Person(
	PersonID int NOT NULL auto_increment,
	First_name varchar(30) NOT NULL,
	Last_name varchar(30),
	DoB DATE,
	Contact int,
	primary key (PersonID),
	foreign key (Contact) references Contact_information(ID) on delete set null);
	

create table Team(
	TeamID INT NOT NULL auto_increment,
	CreationDate DATE,
	Status varchar(7) check (Status in ('Active', 'Retired')),
	Name varchar(30),
	Office int,
	primary key (TeamID),
	foreign key (Office) references Contact_information(ID) on delete set null);
	


create table Team_Member(
	MemberID INT NOT NULL AUTO_INCREMENT,
	TeamID int,
	PersonID int,
	Salary INT,
	HireDate DATE,
	Role varchar(15) check (Category in ('Owner', 'Player', 'Manager', 'Other')),
	Remarks varchar(200),
	primary key (MemberID),
	foreign key (PersonID) references Person(PersonID) on delete set null,
	foreign key (TeamID) references Team(TeamID) on delete set null);
	
	
