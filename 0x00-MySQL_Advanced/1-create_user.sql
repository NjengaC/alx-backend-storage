-- Grants a user all privileges if user exists

CREATE USER
	IF NOT EXISTS 'holberton'@'localhost'
	IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES
	ON *.*
	TO 'holberton'@'localhost';
