drop database if exists myBank;
create database myBank;

USE myBank;


create table Country(
	CountryID int NOT NULL auto_increment,
	countryName varchar(20),
	primary key(CountryID));
	

create table State(
	StateID int NOT NULL auto_increment,
	stateName varchar(20),
	CountryID int,
	primary key(StateID),
	foreign key (CountryID) references Country(CountryID) on delete set null);
	

create table City(
	CityID int NOT NULL auto_increment,
	cityName varchar(20),
	StateID int,
	primary key(CityID),
	foreign key(StateID) references State(StateID) on delete set null);


create table Contact_information(
	ID int NOT NULL auto_increment,
	StreetAddress varchar(40),
	CityID int,
	PostalCode varchar(10),
	Phone varchar(20),
	Mobile varchar(20),
	Email varchar(30),
	primary key(ID),
	foreign key (CityID) references City(CityID) on delete set null);
	

create table account_holder(
	PersonID int NOT NULL auto_increment,
	PAN_number varchar(20) NOT NULL UNIQUE,
	First_name varchar(30) NOT NULL,
	Last_name varchar(30),
	DoB DATE,
	Contact int,
	primary key (PersonID),
	foreign key (Contact) references Contact_information(ID) on delete set null);
	


create table Bank_account(
	AccountID INT NOT NULL auto_increment,
	OpeningDate DATE,
	ClosingDate DATE NULL DEFAULT NULL,
	Status varchar(7) check (Status in ('Active', 'Dormant')),
	AccountHolder int,
	AccountType varchar(10) check (Account_type in ('Savings', 'Current')),
	CurrentBalance BIGINT check (CurrentBalance > 0),
	LastTransactionDate DATE NULL DEFAULT NULL,
	primary key (AccountID),
	foreign key (AccountHolder) references account_holder(PersonID) on delete set null);
	


create table Account_transaction(
	TransactionID INT NOT NULL AUTO_INCREMENT,
	TransactionType varchar(10) check ( Transaction_type in ('Credit','Debit')),
	TransactionDatetime DATE,
	Amount INT,
	AccountID INT,
	Category varchar(15) check (Category in ('Tax', 'salary', 'grocery', 'medical', 'phone', 'bill', 'dining', 'entertainment', 'money transfer' )),
	Remarks varchar(20),
	primary key (TransactionID),
	foreign key (AccountID) references Bank_account(AccountID) on delete set null);
	
	
