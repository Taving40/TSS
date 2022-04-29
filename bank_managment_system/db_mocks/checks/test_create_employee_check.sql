BEGIN TRANSACTION;
CREATE TABLE admin (name text, pass text);
INSERT INTO "admin" VALUES('arpit','123');
CREATE TABLE bank (acc_no int, name text, age int, address text, balance int, account_type text, mobile_number int);
CREATE TABLE staff (name text, pass text,salary int, position text);
INSERT INTO "staff" VALUES('name','password',1,'position');
COMMIT;
