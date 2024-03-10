-- SQL-команды для создания таблиц
CREATE TABLE customers
(
customer_id varchar( 5 ) NOT NULL,
company_name varchar( 100 ) NOT NULL,
contact_name varchar( 100 ) NOT NULL,
CHECK ( customer_id = UPPER( customer_id ) ),
PRIMARY KEY ( customer_id )
);


CREATE TABLE employees
(
employee_id int NOT NULL,
first_name varchar( 30 ) NOT NULL,
last_name varchar ( 50 ) NOT NULL,
title text NOT NULL,
birth_date date NOT NULL,
notes text,
PRIMARY KEY ( employee_id )
);


CREATE TABLE orders
(
order_id int NOT NULL,
customer_id varchar( 5 ) NOT NULL,
employee_id int NOT NULL,
order_date date NOT NULL,
ship_city text NOT NULL,
PRIMARY KEY ( order_id ),
FOREIGN KEY ( customer_id )
REFERENCES customers ( customer_id )
ON DELETE CASCADE,
FOREIGN KEY ( employee_id )
REFERENCES employees ( employee_id )
ON DELETE CASCADE
);
