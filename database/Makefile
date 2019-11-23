all: clean init

init:
	mysql -h localhost -u root < init.sql
	mysql -h localhost -u root < procedures.sql

clean:
	mysql -h localhost -u root < clean.sql
