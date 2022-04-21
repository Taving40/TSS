BEGIN TRANSACTION;
CREATE TABLE admin (name text, pass text);
INSERT INTO "admin" VALUES('arpit','123');
CREATE TABLE bank (acc_no int, name text, age int, address text, balance int, account_type text, mobile_number int);
CREATE TABLE staff (name text, pass text,salary int, position text);
INSERT INTO "staff" VALUES('Popescu Maria','pass',1500,'banker');
INSERT INTO "staff" VALUES('Ionescu Mirela-Oana','pass1234',2500,'loan officer');
COMMIT;
