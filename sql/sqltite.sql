create table service_password (
    id       integer primary key     autoincrement       not null,
    hostname text,
    service  text,
    userid   text,
    userpass text,
    ctime    date   default (datetime('now', 'localtime')),
    utime    date   default (datetime('now', 'localtime'))
);

create inex idx_service_pass_01 on service_password(service, userid);

create table express_resp(
     id       integer primary key     autoincrement       not null,
     server   text  not null,
     pingtime real,
     exetime  date  default(datetime('now', 'localtime'))
);


create table user (
     id       integer primary key    autoincrement     not null,
     userid   text,
     userpass text,
     role     text default "user",   /* admin, user */
     reg_dt   date default(datetime('now', 'localtime')),
     upd_dt   date default(datetime('now', 'localtime'))
);

insert into user (userid, userpass, role) values ('admin', '1tksdbok@#', 'admin');
insert into user (userid, userpass, role) values ('usert', '1tksdbok@#', 'user');

create table server_new (
     id           integer primary key    autoincrement     not null,
     name         text    not null,
     ip           text,
     env          text    default "qa",          /* prod, qa, dev */
     loc          text    default "koreacentral",
     type         text,
     tier         text,
     cpu          integer,
     status       text,
     ssl          text,
     dbtype       text    default "mysql8.0",    /* oracle19.12, mysql8.0 */
     admin        text    default "dbadmin",
     storage      integer,
     storage_grow boolean default(1),
     backup_ret   integer,
     backup_ext   text,
     reg_dt       date default(datetime('now', 'localtime')),
     upd_dt       date default(datetime('now', 'localtime'))
);

insert into server (name, ip, env, dbtype, service) values('qa-gasp-admin-db01', '10.22.0.12', 'qa', 'mysql8.0', 'gasp-admin');
insert into server (name, ip, env, dbtype, service) values('qa-gasp-cert-db01', '10.22.0.10', 'qa', 'mysql8.0', 'gasp-cert');
insert into server (name, ip, env, dbtype, service) values('qa-gasp-common-db01', '10.22.0.4', 'qa', 'mysql8.0', 'gasp-common');
insert into server (name, ip, env, dbtype, service) values('qa-gasp-common-db01', '10.22.0.4', 'qa', 'mysql8.0', 'gasp-common');

drop table service_users;
create table service_users (
     id            integer primary key    autoincrement     not null,
     server_id     integer not null,
     db_name       text    not null,
     service_user  text    not null,
     service_pass  text    not null,
     reg_dt   date default(datetime('now', 'localtime')),
     upd_dt   date default(datetime('now', 'localtime'))
);

insert into service_users (server_id, db_name, service_user, service_pass)
values (2, 'qa_dsp', 'dspgasp', 'qadsp0721!');
insert into service_users (server_id, db_name, service_user, service_pass)
values (3, 'qa_prs', 'spprs', 'qadsp0721!');
insert into service_users (server_id, db_name, service_user, service_pass)
values (3, 'qa_prs', 'spprs', 'qadsp0721!');

create table mysql_tables (
     server_id     integer not null,
     db_name       text    not null,
     table_name    text   not null,
     table_comment text   ,
     table_rows    integer,
     table_size    integer,
     reg_dt   date default(datetime('now', 'localtime')),
     upd_dt   date default(datetime('now', 'localtime')),
     primary key(server_id, db_name, table_name)
);

create index idx_service_pass_01 on service_password(service, userid);

create table mysql_table_stat (
     server_id     integer not null,
     db_count      integer,
     table_count   integer,
     table_data    integer,
     reg_dt   date default(datetime('now', 'localtime')),
     upd_dt   date default(datetime('now', 'localtime')),
     primary key(server_id, reg_dt)
);
