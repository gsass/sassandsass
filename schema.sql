drop table if exists pages;
create table pages (
  id Integer not null auto_increment,
  link_alias text primary key not null,
  title text not null,
  blurb text not null,
  imagename text,
  content text
);

drop table is exists nav;
create table nav (
  id Integer primary key not null,
  rank Integer not null,
  children text not null
);
