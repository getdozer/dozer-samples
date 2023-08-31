#!/bin/sh
set -e
r=`mysql -u root --password=mysql --batch --silent --database=Chinook -e 'SELECT COUNT(*) > 0 FROM ready'`
[ "$r" = 1 ]