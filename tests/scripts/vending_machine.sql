DROP SCHEMA IF EXISTS vending_tracker;
CREATE SCHEMA vending_tracker;
USE vending_tracker;
drop table if exists products;
create table products(product_name varchar(255) not null,price int not null,product_id int auto_increment primary key);
drop table if exists vending_machine;
create table vending_machine(vending_machine_id int auto_increment primary key,location varchar(255) not null, name varchar(255) not null);
drop table if exists listing;
create table listing(product_id int not null,vending_machine_id int not null,quantity int not null,primary key (product_id, vending_machine_id),constraint product_id foreign key (product_id) references products (product_id), constraint vending_machine_id foreign key (vending_machine_id) references vending_machine (vending_machine_id));