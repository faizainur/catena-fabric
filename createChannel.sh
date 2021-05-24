#!/bin/bash

export FABRIC_CFG_PATH=${PWD}/config

# User Profiles Channel
configtxgen -profile KYCFinancialChannel -outputBlock ./channel-artifacts/devuserprofileschannel.block -channelID devuserprofileschannel 
# Credit Record Channel
configtxgen -profile KYCFinancialChannel -outputBlock ./channel-artifacts/devcreditrecordchannel.block -channelID devcreditrecordchannel

export ORDERER_CA=${PWD}/organizations/ordererOrganizations/catena.id/orderers/orderer.catena.id/msp/tlscacerts/tlsca.catena.id-cert.pem
export ORDERER_ADMIN_TLS_SIGN_CERT=${PWD}/organizations/ordererOrganizations/catena.id/orderers/orderer.catena.id/tls/server.crt
export ORDERER_ADMIN_TLS_PRIVATE_KEY=${PWD}/organizations/ordererOrganizations/catena.id/orderers/orderer.catena.id/tls/server.key

osnadmin channel join --channelID devuserprofileschannel --config-block ./channel-artifacts/devuserprofileschannel.block -o localhost:7053 --ca-file "$ORDERER_CA" --client-cert "$ORDERER_ADMIN_TLS_SIGN_CERT" --client-key "$ORDERER_ADMIN_TLS_PRIVATE_KEY"
osnadmin channel join --channelID devcreditrecordchannel --config-block ./channel-artifacts/devcreditrecordchannel.block -o localhost:7053 --ca-file "$ORDERER_CA" --client-cert "$ORDERER_ADMIN_TLS_SIGN_CERT" --client-key "$ORDERER_ADMIN_TLS_PRIVATE_KEY"

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="BankAMSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/bankA.catena.id/peers/peer0.bankA.catena.id/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/bankA.catena.id/users/AdminBankA@bankA.catena.id/msp
export CORE_PEER_ADDRESS=localhost:7051

peer channel join -b ./channel-artifacts/devcreditrecordchannel.block
peer channel join -b ./channel-artifacts/devuserprofileschannel.block

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="BankBMSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/bankB.catena.id/peers/peer0.bankB.catena.id/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/bankB.catena.id/users/AdminBankB@bankB.catena.id/msp
export CORE_PEER_ADDRESS=localhost:9051

peer channel join -b ./channel-artifacts/devcreditrecordchannel.block
peer channel join -b ./channel-artifacts/devuserprofileschannel.block

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="GovMSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/gov.catena.id/peers/peer0.gov.catena.id/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/gov.catena.id/users/AdminGov@gov.catena.id/msp
export CORE_PEER_ADDRESS=localhost:10051

peer channel join -b ./channel-artifacts/devcreditrecordchannel.block
peer channel join -b ./channel-artifacts/devuserprofileschannel.block