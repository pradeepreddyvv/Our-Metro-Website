CREATE TABLE members
(
  email_id VARCHAR(30) NOT NULL,
  name VARCHAR(20) NOT NULL,
  gender VARCHAR(10) NOT NULL,
  password VARCHAR(30) NOT NULL,
  PRIMARY KEY (email_id)
);

CREATE TABLE metro_card
(
  card_id INT NOT NULL,
  balance INT NOT NULL,
  start VARCHAR(30) NOT NULL,
  destination VARCHAR(30) NOT NULL,
  s_time VARCHAR(30) NOT NULL,
  d_time VARCHAR(30) NOT NULL,
  email_id VARCHAR(30) NOT NULL,
  PRIMARY KEY (card_id),
  FOREIGN KEY (email_id) REFERENCES members(email_id)
);

CREATE TABLE admins
(
  admin_id INT NOT NULL,
  admin_name VARCHAR(20) NOT NULL,
  email_id VARCHAR(30) NOT NULL,
  PRIMARY KEY (admin_id),
  FOREIGN KEY (email_id) REFERENCES members(email_id)
);

CREATE TABLE lines
(
  line_id VARCHAR(10) NOT NULL,
  color VARCHAR(3) NOT NULL,
  start_station VARCHAR(30) NOT NULL,
  end_station VARCHAR(30) NOT NULL,
  PRIMARY KEY (line_id)
);

CREATE TABLE metro
(
  metro_id INT NOT NULL,
  line_id VARCHAR(10) NOT NULL,
  PRIMARY KEY (metro_id),
  FOREIGN KEY (line_id) REFERENCES lines(line_id)
);

CREATE TABLE phoneno
(
  p_no VARCHAR(15) NOT NULL,
  p_no2 VARCHAR(15) NOT NULL,
  email_id VARCHAR(30) NOT NULL,
  FOREIGN KEY (email_id) REFERENCES members(email_id)
);

CREATE TABLE payment
(
  payment_id INT NOT NULL,
  status VARCHAR(20) NOT NULL,
  card_id INT NOT NULL,
  PRIMARY KEY (payment_id),
  FOREIGN KEY (card_id) REFERENCES metro_card(card_id)
);

CREATE TABLE station
(
  station_id INT NOT NULL,
  station_name VARCHAR(30) NOT NULL,
  line_id VARCHAR(10) NOT NULL,
  PRIMARY KEY (station_id),
  FOREIGN KEY (line_id) REFERENCES lines(line_id)
);

CREATE TABLE crossing
(
  cross_id INT NOT NULL,
  line_1 VARCHAR(10) NOT NULL,
  line_2 VARCHAR(10) NOT NULL,
  station_id INT NOT NULL,
  PRIMARY KEY (cross_id),
  FOREIGN KEY (station_id) REFERENCES station(station_id)
);

CREATE TABLE users
(
  user_id INT NOT NULL,
  gender VARCHAR(10) NOT NULL,
  station_id INT NOT NULL,
  PRIMARY KEY (user_id),
  FOREIGN KEY (station_id) REFERENCES station(station_id)
);

CREATE TABLE ticket
(
  ticket_id INT NOT NULL,
  date_cur VARCHAR(15) NOT NULL,
  start_time VARCHAR(10) NOT NULL,
  end_time VARCHAR(10) NOT NULL,
  fare INT NOT NULL,
  start VARCHAR(30) NOT NULL,
  destination VARCHAR(30) NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (ticket_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE platform
(
  platform_no INT NOT NULL,
  arrival_time VARCHAR(10) NOT NULL,
  departure_time VARCHAR(10) NOT NULL,
  waiting_time VARCHAR(10) NOT NULL,
  station_id INT NOT NULL,
  user_id INT NOT NULL,
  FOREIGN KEY (station_id) REFERENCES station(station_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE boards
(
  metro_id INT NOT NULL,
  user_id INT NOT NULL,
  station_id INT NOT NULL,
  FOREIGN KEY (metro_id) REFERENCES metro(metro_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (station_id) REFERENCES station(station_id)
);
CREATE TABLE report
(
  report_subject VARCHAR(50) NOT NULL,
  report VARCHAR(300) NOT NULL,
  email_id VARCHAR(30) NOT NULL,
  FOREIGN KEY (email_id) REFERENCES members(email_id)
);