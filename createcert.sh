#!/bin/sh

#small script to create self signed cert for the app to work...
# based on: "http://www.akadia.com/services/ssh_test_certificate.html"
#it's very basic

#Name of cert file:
FILENAME="dynamicip_server"

#target fields entry cmdline: -subj "/C=GB/ST=London/L=London/O=Global Security/OU=IT Department/CN=example.com"
#series of commands:
echo "openssl genrsa -des3 -passout pass:1234 -out ${FILENAME}.key 1024"
openssl genrsa -des3 -passout pass:1234 -out ${FILENAME}.key 1024
echo "openssl req -new -key ${FILENAME}.key -passin pass:1234 -out ${FILENAME}.csr"
openssl req -new -key ${FILENAME}.key -passin pass:1234 -out ${FILENAME}.csr
echo "cp ${FILENAME}.key ${FILENAME}.key.org"
cp ${FILENAME}.key ${FILENAME}.key.org
echo "openssl rsa -in ${FILENAME}.key.org -passin pass:1234 -out ${FILENAME}.key"
openssl rsa -in ${FILENAME}.key.org -passin pass:1234 -out ${FILENAME}.key
echo "openssl x509 -req -days 365 -in ${FILENAME}.csr -signkey ${FILENAME}.key -out ${FILENAME}.crt"
openssl x509 -req -days 365 -in ${FILENAME}.csr -signkey ${FILENAME}.key -out ${FILENAME}.crt

