drop table if exists pages;
create table pages (
  id Integer not null auto_increment
  title text primary key not null,
  blurb text not null,
  imagename text,
  content text
);

drop table is exists nav;
create table nav (
  id Integer not null auto_increment
  children text not null
);
