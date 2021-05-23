docker container stop peer0.bankB.catena.id peer0.gov.catena.id peer0.bankA.catena.id orderer.catena.id ca_bankAOrg ca_bankBOrg ca_orderer cli ca_govOrg
docker container rm peer0.bankB.catena.id peer0.gov.catena.id peer0.bankA.catena.id orderer.catena.id ca_bankAOrg ca_bankBOrg ca_orderer cli ca_govOrg

sudo rm -rf channel-artifacts system-genesis-block/ organizations/ordererOrganizations organizations/peerOrganizations

sudo rm -rf organizations/fabric-ca/bankAOrg/IssuerPublicKey organizations/fabric-ca/bankAOrg/IssuerRevocationPublicKey organizations/fabric-ca/bankAOrg/ca-cert.pem organizations/fabric-ca/bankAOrg/fabric-ca-server.db organizations/fabric-ca/bankAOrg/msp organizations/fabric-ca/bankAOrg/tls-cert.pem
sudo rm -rf organizations/fabric-ca/bankBOrg/IssuerPublicKey organizations/fabric-ca/bankBOrg/IssuerRevocationPublicKey organizations/fabric-ca/bankBOrg/ca-cert.pem organizations/fabric-ca/bankBOrg/fabric-ca-server.db organizations/fabric-ca/bankBOrg/msp organizations/fabric-ca/bankBOrg/tls-cert.pem
sudo rm -rf organizations/fabric-ca/ordererOrg/IssuerPublicKey organizations/fabric-ca/ordererOrg/IssuerRevocationPublicKey organizations/fabric-ca/ordererOrg/ca-cert.pem organizations/fabric-ca/ordererOrg/fabric-ca-server.db organizations/fabric-ca/ordererOrg/msp organizations/fabric-ca/ordererOrg/tls-cert.pem
sudo rm -rf organizations/fabric-ca/govOrg/IssuerPublicKey organizations/fabric-ca/govOrg/IssuerRevocationPublicKey organizations/fabric-ca/govOrg/ca-cert.pem organizations/fabric-ca/govOrg/fabric-ca-server.db organizations/fabric-ca/govOrg/msp organizations/fabric-ca/govOrg/tls-cert.pem
