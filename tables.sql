CREATE TABLE userInformation (
  netid varchar(20) NOT NULL,
  name varchar NOT NULL,
  email varchar(30), 
  phone int,
  description varchar NOT NULL,
  address varchar NOT NULL,
    PRIMARY KEY (netid)
);

CREATE TABLE coordinates (
  netid varchar(20) NOT NULL,
  address varchar(200) NOT NULL,
  latitude real NOT NULL,
  longitude real NOT NULL,
    PRIMARY KEY (netid)
);

