# database

- install the following packages: `sudo apt install sqlite3 unixodbc libsqliteodbc sqlitebrowser`
- edit file **/etc/odbcinst.ini**
```
[SQLite3]
Description=SQLite3 ODBC Driver
Driver=/usr/lib/x86_64-linux-gnu/odbc/libsqlite3odbc.so
Setup=/usr/lib/x86_64-linux-gnu/odbc/libsqlite3odbc.so
UsageCount=1
```
or 
```
[SQLite3]
Description=SQLite3 ODBC Driver
Driver=libsqlite3odbc.so
Setup=libsqlite3odbc.so
UsageCount=1
```