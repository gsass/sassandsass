drop table if exists pages;
create table pages (
  id Integer primary key not null,
  link_alias text unique not null,
  title text not null,
  blurb text not null,
  imagename text,
  content text
);

drop table if exists nav;
create table nav (
  id Integer primary key not null,
  rank Integer unique not null,
  head Boolean default False,
  children text not null
);

drop table if exists users;
create table users (
  userid text unique not null,
  tokenhash text,
  active Boolean default False
);
