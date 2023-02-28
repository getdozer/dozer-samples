#!/bin/bash

mkdir -p tmpdir
cd tmpdir

# Uncomment the following lines for a larger data set
# curl https://edu.postgrespro.com/demo-big-en.zip --output ./demo-big-en.zip
# unzip demo-big-en.zip
# cp ./demo-big-en-20170815.sql ../data/init.sql

curl https://edu.postgrespro.com/demo-small-en.zip --output ./demo-small-en.zip
unzip demo-small-en.zip
rm -rf ../data
mkdir -p ../data
cp ./demo-small-en-20170815.sql ../data/init.sql
rm -rf tmpdir
