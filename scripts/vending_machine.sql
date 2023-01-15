create table products
(
    product_name varchar(255) not null,
    price        int          not null,
    product_id   int auto_increment
        primary key
);

create table vending_machine
(
    vending_machine_id int auto_increment
        primary key,
    location           varchar(255) not null
);

create table listing
(
    listing_id         int auto_increment
        primary key,
    product_id         int not null,
    vending_machine_id int not null,
    quantity           int not null,
    constraint product_id
        foreign key (product_id) references products (product_id),
    constraint vending_machine_id
        foreign key (vending_machine_id) references vending_machine (vending_machine_id)
);