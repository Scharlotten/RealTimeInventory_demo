CREATE TABLE customers(
  id serial primary key not null,
  first_name varchar(64),
  last_name varchar(64),
  zipcode varchar(14),
  country varchar(64),
  address varchar(64)
);