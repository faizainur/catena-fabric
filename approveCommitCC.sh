#!/bin/bash

export PATH=$PATH:${PWD}/bin
export FABRIC_CFG_PATH=${PWD}/config

# Export chaincode package id
# input here
export CC_PACKAGE_ID=

# Approve chaincode definition
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="GovMSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/gov.catena.id/peers/peer0.gov.catena.id/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/gov.catena.id/users/AdminGov@gov.catena.id/msp
export CORE_PEER_ADDRESS=localhost:10051

peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.catena.id --channelID userprofileschannel --name cckyc --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/catena.id/orderers/orderer.catena.id/msp/tlscacerts/tlsca.catena.id-cert.pem

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="BankAMSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/bankA.catena.id/peers/peer0.bankA.catena.id/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/bankA.catena.id/users/AdminBankA@bankA.catena.id/msp
export CORE_PEER_ADDRESS=localhost:7051

peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.catena.id --channelID userprofileschannel --name cckyc --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/catena.id/orderers/orderer.catena.id/msp/tlscacerts/tlsca.catena.id-cert.pem

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="BankBMSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/bankB.catena.id/peers/peer0.bankB.catena.id/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/bankB.catena.id/users/AdminBankB@bankB.catena.id/msp
export CORE_PEER_ADDRESS=localhost:9051

peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.catena.id --channelID userprofileschannel --name cckyc --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/catena.id/orderers/orderer.catena.id/msp/tlscacerts/tlsca.catena.id-cert.pem

# Commit chaincode
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="GovMSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/gov.catena.id/peers/peer0.gov.catena.id/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/gov.catena.id/users/AdminGov@gov.catena.id/msp
export CORE_PEER_ADDRESS=localhost:10051

peer lifecycle chaincode checkcommitreadiness --channelID userprofileschannel --name cckyc --version 1.1 --sequence 1 --tls --cafile "${PWD}/organizations/ordererOrganizations/catena.id/orderers/orderer.catena.id/msp/tlscacerts/tlsca.catena.id-cert.pem" --output json

peer lifecycle chaincode commit -o localhost:7050 --ordererTLSHostnameOverride orderer.catena.id --channelID userprofileschannel --name cckyc --version 1.0 --sequence 1 --tls --cafile "${PWD}/organizations/ordererOrganizations/catena.id/orderers/orderer.catena.id/msp/tlscacerts/tlsca.catena.id-cert.pem" --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/bankA.catena.id/peers/peer0.bankA.catena.id/tls/ca.crt" --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/bankB.catena.id/peers/peer0.bankB.catena.id/tls/ca.crt" --peerAddresses localhost:10051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/gov.catena.id/peers/peer0.gov.catena.id/tls/ca.crt"