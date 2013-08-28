drop table if exists pages;
create table pages (
  title text primary key not null,
  blurb text not null,
  imagename text,
  content text
);
