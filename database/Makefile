all: clean init

init:
	mysql -h localhost -u root < init.sql

clean:
	mysql -h localhost -u root < clean.sql
