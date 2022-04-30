BEGIN TRANSACTION;
CREATE TABLE admin (name text, pass text);
INSERT INTO "admin" VALUES('arpit','123');
CREATE TABLE bank (acc_no int, name text, age int, address text, balance int, account_type text, mobile_number int);
INSERT INTO "bank" VALUES(1,'name',1,'address',1,'account_type',1);
CREATE TABLE staff (name text, pass text,salary int, position text);
COMMIT;
