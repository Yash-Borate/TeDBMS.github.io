create table supplier(
	supplier_id int unsigned auto_increment,
	supplier_name varchar(50) not null,
	supplier_city varchar(50) not null,
	city_pincode numeric(6,0) not null,
	primary key (supplier_id)
);


create table employee(
	emp_id int unsigned auto_increment,
	emp_name varchar(50) not null,
	emp_gender varchar(10) not null,
	emp_age numeric(2,0) not null,
	emp_salary int unsigned not null,
	primary key (emp_id)
);


create table medicine(
	med_id int unsigned auto_increment,
	med_name varchar(50) not null,
	price int unsigned not null,
	primary key (med_id)
);


create table stock (
	stock_id int unsigned auto_increment, 
	quantity numeric(5,0) not null, 
	price int unsigned not null, 
	mfg_date date not null, 
	exp_date date not null, 
	stock_arrival_date date not null, 
	supplier_id int unsigned, 
	med_id int unsigned, 
	curr_quantity numeric(5,0) not null,
	primary key (stock_id), foreign key (med_id) references medicine(med_id) on delete cascade, 
	foreign key (supplier_id) references supplier(supplier_id) on delete cascade
);

create table bill (
	bill_id int unsigned auto_increment, 
	cust_name varchar(50) not null, 
	med_name varchar(50) not null, 
	quantity int unsigned not null, 
	price int unsigned not null, 
	bill_date date not null,
	primary key (bill_id)
);





