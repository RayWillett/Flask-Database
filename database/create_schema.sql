CREATE TABLE EMPLOYEE (
	enumb INT PRIMARY KEY,
	fname TEXT NOT NULL,
	lname TEXT NOT NULL
);
CREATE TABLE CUSTOMER (
	fname TEXT NOT NULL,
	lname TEXT NOT NULL,
	phone TEXT PRIMARY KEY
);
CREATE TABLE PET (
	name TEXT NOT NULL,
	date_in INT,
	date_out INT NOT NULL,
	owner TEXT,
  	pen INT,
	FOREIGN KEY(owner) REFERENCES CUSTOMER(phone),
  	FOREIGN KEY(pen) REFERENCES EMPLOYEE(id)
);
CREATE TABLE PEN (
	id INT PRIMARY KEY,
	fill INT NOT NULL,
	capacity INT NOT NULL,
	finished INT NOT NULL,
	worker INT,
	FOREIGN KEY(worker) REFERENCES EMPLOYEE(enumb),
	CHECK (capacity > 0 AND finished >= 0 AND finished <= 1)
);
CREATE TABLE SHIFT (
	day INT NOT NULL,
	snum INT,
	worker INT,
	FOREIGN KEY(worker) REFERENCES EMPLOYEE(enumb)
	PRIMARY KEY(day, snum)
	CHECK(snum > 0 AND snum < 4)
);