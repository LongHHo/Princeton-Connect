CREATE TABLE userInformation (
  netid varchar(20) NOT NULL,
  name varchar(50) NOT NULL,
  email varchar(30), 
  phone int,
  description varchar(300) NOT NULL,
  address varchar(200) NOT NULL,
    PRIMARY KEY (netid)
);

CREATE TABLE coordinates (
  netid varchar(20) NOT NULL,
  address varchar(200) NOT NULL,
  latitude real NOT NULL,
  longitude real NOT NULL,
    PRIMARY KEY (netid)
);

