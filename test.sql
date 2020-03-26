CREATE TABLE `userInformation` (
  `netid` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(30) NOT NULL,
  `phone` int(11) NOT NULL,
  `description` varchar(300) NOT NULL,
   `address` varchar(200) NOT NULL,
    PRIMARY KEY (`netid`)
)
