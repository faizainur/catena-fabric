#!/bin/bash

export PATH=$PATH:${PWD}/bin
export FABRIC_CFG_PATH=${PWD}/config

cd chaincodes/creditcc && GO111MODULE=on go mod vendor
cd ../..

# Packaging chaincode
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="GovMSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/gov.catena.id/peers/peer0.gov.catena.id/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/gov.catena.id/users/AdminGov@gov.catena.id/msp
export CORE_PEER_ADDRESS=localhost:10051

peer lifecycle chaincode package creditcc.tar.gz --path chaincodes/creditcc --lang golang --label creditcc_1.14

# Installing chaincode into peers
peer lifecycle chaincode install creditcc.tar.gz

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="BankAMSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/bankA.catena.id/peers/peer0.bankA.catena.id/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/bankA.catena.id/users/AdminBankA@bankA.catena.id/msp
export CORE_PEER_ADDRESS=localhost:7051

peer lifecycle chaincode install creditcc.tar.gz

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="BankBMSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/bankB.catena.id/peers/peer0.bankB.catena.id/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/bankB.catena.id/users/AdminBankB@bankB.catena.id/msp
export CORE_PEER_ADDRESS=localhost:9051

peer lifecycle chaincode install creditcc.tar.gz
