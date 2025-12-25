#!/bin/bash

if [ -f onekiwi.sqlite ]; then
    echo "remove onekiwi.sqlite"
    rm onekiwi.sqlite
fi

CSV=`find -name '*.csv' | xargs -I{} basename {} ".csv"`

for lib in ${CSV}; do
	sqlite3 --csv ./onekiwi.sqlite ".import ${lib}.csv ${lib}" || return 1
done


