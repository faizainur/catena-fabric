#!/bin/bash

function one_line_pem {
    echo "`awk 'NF {sub(/\\n/, ""); printf "%s\\\\\\\n",$0;}' $1`"
}

function json_ccp {
    local PP=$(one_line_pem $4)
    local CP=$(one_line_pem $5)
    sed -e "s/\${ORG}/$1/" \
        -e "s/\${P0PORT}/$2/" \
        -e "s/\${CAPORT}/$3/" \
        -e "s#\${PEERPEM}#$PP#" \
        -e "s#\${CAPEM}#$CP#" \
        organizations/ccp-template.json
}

function yaml_ccp {
    local PP=$(one_line_pem $4)
    local CP=$(one_line_pem $5)
    sed -e "s/\${ORG}/$1/" \
        -e "s/\${P0PORT}/$2/" \
        -e "s/\${CAPORT}/$3/" \
        -e "s#\${PEERPEM}#$PP#" \
        -e "s#\${CAPEM}#$CP#" \
        organizations/ccp-template.yaml | sed -e $'s/\\\\n/\\\n          /g'
}

ORG=bankA
P0PORT=7051
CAPORT=7054
PEERPEM=organizations/peerOrganizations/bankA.catena.id/tlsca/tlsca.bankA.catena.id-cert.pem
CAPEM=organizations/peerOrganizations/bankA.catena.id/ca/ca.bankA.catena.id-cert.pem

echo "$(json_ccp $ORG $P0PORT $CAPORT $PEERPEM $CAPEM)" > organizations/peerOrganizations/bankA.catena.id/connection-bankA.json
echo "$(yaml_ccp $ORG $P0PORT $CAPORT $PEERPEM $CAPEM)" > organizations/peerOrganizations/bankA.catena.id/connection-bankA.yaml

ORG=bankB
P0PORT=9051
CAPORT=8054
PEERPEM=organizations/peerOrganizations/bankB.catena.id/tlsca/tlsca.bankB.catena.id-cert.pem
CAPEM=organizations/peerOrganizations/bankB.catena.id/ca/ca.bankB.catena.id-cert.pem

echo "$(json_ccp $ORG $P0PORT $CAPORT $PEERPEM $CAPEM)" > organizations/peerOrganizations/bankB.catena.id/connection-bankB.json
echo "$(yaml_ccp $ORG $P0PORT $CAPORT $PEERPEM $CAPEM)" > organizations/peerOrganizations/bankB.catena.id/connection-bankB.yaml

ORG=gov
P0PORT=10051
CAPORT=10054
PEERPEM=organizations/peerOrganizations/gov.catena.id/tlsca/tlsca.gov.catena.id-cert.pem
CAPEM=organizations/peerOrganizations/gov.catena.id/ca/ca.gov.catena.id-cert.pem

echo "$(json_ccp $ORG $P0PORT $CAPORT $PEERPEM $CAPEM)" > organizations/peerOrganizations/gov.catena.id/connection-gov.json
echo "$(yaml_ccp $ORG $P0PORT $CAPORT $PEERPEM $CAPEM)" > organizations/peerOrganizations/gov.catena.id/connection-gov.yaml
