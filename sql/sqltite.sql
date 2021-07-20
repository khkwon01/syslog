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