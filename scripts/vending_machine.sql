create schema if not exists vending_tracker;
use vending_tracker
create table if not exists products(product_name varchar(255) not null,price        int          not null,product_id   int auto_incrementprimary key);
create table if not exists vending_machine(vending_machine_id int auto_incrementprimary key,location           varchar(255) not null,name               varchar(255) not null);
create table if not exists listing(product_id         int not null,vending_machine_id int not null,quantity           int not null,primary key (product_id, vending_machine_id),constraint product_idforeign key (product_id) references products (product_id) constraint vending_machine_idforeign key (vending_machine_id) references vending_machine (vending_machine_id));
