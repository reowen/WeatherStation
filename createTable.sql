CREATE TABLE IF NOT EXISTS `bmp180` (
  `reading_id` int(255) NOT NULL AUTO_INCREMENT,
  `temperature_c` double NOT NULL,
  `temperature_f` double NOT NULL,
  `barometric_pressure` varchar(20) NOT NULL,
  `altitude` varchar(20) NOT NULL,
  `dateMeasured` date NOT NULL,
  `hourMeasured` int(128) NOT NULL,
  `timeBlock` int(128) NOT NULL,
  PRIMARY KEY (`reading_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1  ;

CREATE TABLE IF NOT EXISTS `dht22` (
  `dht_id` int(255) NOT NULL AUTO_INCREMENT,
  `reading_id` int(20) NOT NULL,
  `temperature_c` double NOT NULL,
  `temperature_f` double NOT NULL,
  `humidity` varchar(20) NOT NULL,
  `dateMeasured` date NOT NULL,
  `hourMeasured` int(128) NOT NULL,
  `timeBlock` int(128) NOT NULL,
  PRIMARY KEY (`dht_id`),
  FOREIGN KEY (`reading_id`) REFERENCES bmp180(`reading_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
