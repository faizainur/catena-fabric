# This module contains functions used to generate
# Crypto materials for initiating a node in Hyperledger Fabric
# Supported method: CA

import subprocess
import os
import shutil

COMPOSE_FILE_CA = "docker/docker-compose-ca.yaml"

def cagenHello(): 
    print("Hello Cagen")

def initContainer():
    print("Generating certificates using Fabric CA")
    subprocess.run(["docker-compose", "-f", COMPOSE_FILE_CA, "up", "-d"])
    subprocess.run(["docker", "ps"])

def createBankAOrg():
    caClientHomePath =  os.path.join(os.getcwd(), "organizations", "peerOrganizations", "bankA.catena.id")
    os.makedirs(caClientHomePath)
    os.environ['FABRIC_CA_CLIENT_HOME'] = caClientHomePath

    tlsCertFilePath = os.path.join(os.getcwd(), "organizations", "fabric-ca", "bankAOrg", "tls-cert.pem")
    subprocess.run(["fabric-ca-client", "enroll", "-u", "https://admin:adminpw@localhost:7054",
                    "--caname", "ca-bankAOrg", "--tls.certfiles", tlsCertFilePath])
    
    configYamlPath = os.path.join(os.getcwd(), caClientHomePath, "msp", "config.yaml")
    configNodeOUs = """NodeOUs:
  Enable: true
  ClientOUIdentifier:
    Certificate: cacerts/localhost-7054-ca-bankAOrg.pem
    OrganizationalUnitIdentifier: client
  PeerOUIdentifier:
    Certificate: cacerts/localhost-7054-ca-bankAOrg.pem
    OrganizationalUnitIdentifier: peer
  AdminOUIdentifier:
    Certificate: cacerts/localhost-7054-ca-bankAOrg.pem
    OrganizationalUnitIdentifier: admin
  OrdererOUIdentifier:
    Certificate: cacerts/localhost-7054-ca-bankAOrg.pem
    OrganizationalUnitIdentifier: orderer
    """

    # subprocess.run(["echo", configNodeOUs, ">", configYamlPath])
    configFile = open(configYamlPath, "w+")
    configFile.write(configNodeOUs)
    configFile.close()

    # Registering peer0
    registerCa("ca-bankAOrg", "peer0", "peer0pw", "peer", tlsCertFilePath)

    # Registering peer0
    registerCa("ca-bankAOrg", "user1", "user1pw", "client", tlsCertFilePath)

    # Registering peer0
    registerCa("ca-bankAOrg", "adminBankA", "adminBankApw", "admin", tlsCertFilePath)

    # Generate peer0 MSP
    generateMsp("https://peer0:peer0pw@localhost:7054", "ca-bankAOrg",
                os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "msp"),
                "peer0.bankA.catena.id",
                tlsCertFilePath)
    subprocess.run(["cp", 
        os.path.join(caClientHomePath, "msp", "config.yaml"),
        os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "msp", "config.yaml"),
    ])

    # Generate peer0 TLS Certificates
    generateTlsCert("https://peer0:peer0pw@localhost:7054", "ca-bankAOrg",
                os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "tls"),
                "tls",
                "peer0.bankA.catena.id",
                "localhost",
                tlsCertFilePath)
    
#    shutil.copyfile(
#         os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "tls", "tlscacerts"),
#    )

    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "tls", "tlscacerts")),
        os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "tls", "ca.crt"),
    ])

    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "tls", "signcerts")),
        os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "tls", "server.crt"),
    ])
    
    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "tls", "keystore")),
        os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "tls", "server.key"),
    ])

    os.makedirs(os.path.join(caClientHomePath, "msp", "tlscacerts"))
    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "tls", "tlscacerts")) ,
        os.path.join(caClientHomePath, "msp", "ca.crt"),
    ])

    os.makedirs(os.path.join(caClientHomePath, "tlsca"))
    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "tls", "tlscacerts")),
        os.path.join(caClientHomePath, "tlsca", "tlsca.peer0.bankA.catena.id-cert.pem"),
    ])

    os.makedirs(os.path.join(caClientHomePath, "ca"))
    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "msp", "cacerts")),
        os.path.join(caClientHomePath, "ca", "ca.bankA.catena.id-cert.pem"),
    ])

    # Generating adminBankA MSP
    generateMsp("https://adminBankA:adminBankApw@localhost:7054", "ca-bankAOrg",
                os.path.join(caClientHomePath, "users", "AdminBankA@bankA.catena.id", "msp"),
                None,
                tlsCertFilePath)
    subprocess.run(["cp", 
        os.path.join(caClientHomePath, "msp", "config.yaml"),
        os.path.join(caClientHomePath, "users", "AdminBankA@bankA.catena.id", "msp", "config.yaml"),
    ])

    # Generating user1 MSP
    generateMsp("https://user1:user1pw@localhost:7054", "ca-bankAOrg",
                os.path.join(caClientHomePath, "users", "User1@bankA.catena.id", "msp"),
                None,
                tlsCertFilePath)
    subprocess.run(["cp", 
        os.path.join(caClientHomePath, "msp", "config.yaml"),
        os.path.join(caClientHomePath, "users", "User1@bankA.catena.id", "msp", "config.yaml"),
    ])

def createBankBOrg():
    caClientHomePath =  os.path.join(os.getcwd(), "organizations", "peerOrganizations", "bankB.catena.id")
    os.makedirs(caClientHomePath)
    os.environ['FABRIC_CA_CLIENT_HOME'] = caClientHomePath

    tlsCertFilePath = os.path.join(os.getcwd(), "organizations", "fabric-ca", "bankBOrg", "tls-cert.pem")
    subprocess.run(["fabric-ca-client", "enroll", "-u", "https://admin:adminpw@localhost:8054",
                    "--caname", "ca-bankBOrg", "--tls.certfiles", tlsCertFilePath])
    
    configYamlPath = os.path.join(os.getcwd(), caClientHomePath, "msp", "config.yaml")
    configNodeOUs = """NodeOUs:
  Enable: true
  ClientOUIdentifier:
    Certificate: cacerts/localhost-8054-ca-bankBOrg.pem
    OrganizationalUnitIdentifier: client
  PeerOUIdentifier:
    Certificate: cacerts/localhost-8054-ca-bankBOrg.pem
    OrganizationalUnitIdentifier: peer
  AdminOUIdentifier:
    Certificate: cacerts/localhost-8054-ca-bankBOrg.pem
    OrganizationalUnitIdentifier: admin
  OrdererOUIdentifier:
    Certificate: cacerts/localhost-8054-ca-bankBOrg.pem
    OrganizationalUnitIdentifier: orderer
    """

    # subprocess.run(["echo", configNodeOUs, ">", configYamlPath])
    configFile = open(configYamlPath, "w+")
    configFile.write(configNodeOUs)
    configFile.close()

    # Registering peer0
    registerCa("ca-bankBOrg", "peer0", "peer0pw", "peer", tlsCertFilePath)

    # Registering peer0
    registerCa("ca-bankBOrg", "user1", "user1pw", "client", tlsCertFilePath)

    # Registering peer0
    registerCa("ca-bankBOrg", "adminBankB", "adminBankBpw", "admin", tlsCertFilePath)

    # Generate peer0 MSP
    generateMsp("https://peer0:peer0pw@localhost:8054", "ca-bankBOrg",
                os.path.join(caClientHomePath, "peers", "peer0.bankB.catena.id", "msp"),
                "peer0.bankB.catena.id",
                tlsCertFilePath)
    subprocess.run(["cp", 
        os.path.join(caClientHomePath, "msp", "config.yaml"),
        os.path.join(caClientHomePath, "peers", "peer0.bankB.catena.id", "msp", "config.yaml"),
    ])

    # Generate peer0 TLS Certificates
    generateTlsCert("https://peer0:peer0pw@localhost:8054", "ca-bankBOrg",
                os.path.join(caClientHomePath, "peers", "peer0.bankB.catena.id", "tls"),
                "tls",
                "peer0.bankB.catena.id",
                "localhost",
                tlsCertFilePath)
    
#    shutil.copyfile(
#         os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "tls", "tlscacerts"),
#    )

    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "peers", "peer0.bankB.catena.id", "tls", "tlscacerts")),
        os.path.join(caClientHomePath, "peers", "peer0.bankB.catena.id", "tls", "ca.crt"),
    ])

    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "peers", "peer0.bankB.catena.id", "tls", "signcerts")),
        os.path.join(caClientHomePath, "peers", "peer0.bankB.catena.id", "tls", "server.crt"),
    ])
    
    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "peers", "peer0.bankB.catena.id", "tls", "keystore")),
        os.path.join(caClientHomePath, "peers", "peer0.bankB.catena.id", "tls", "server.key"),
    ])

    os.makedirs(os.path.join(caClientHomePath, "msp", "tlscacerts"))
    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "peers", "peer0.bankB.catena.id", "tls", "tlscacerts")),
        os.path.join(caClientHomePath, "msp", "ca.crt"),
    ])

    os.makedirs(os.path.join(caClientHomePath, "tlsca"))
    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "peers", "peer0.bankB.catena.id", "tls", "tlscacerts")),
        os.path.join(caClientHomePath, "tlsca", "tlsca.peer0.bankB.catena.id-cert.pem"),
    ])

    os.makedirs(os.path.join(caClientHomePath, "ca"))
    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "peers", "peer0.bankB.catena.id", "msp", "cacerts")),
        os.path.join(caClientHomePath, "ca", "ca.bankB.catena.id-cert.pem"),
    ])

    # Generating adminBankA MSP
    generateMsp("https://adminBankB:adminBankBpw@localhost:8054", "ca-bankBOrg",
                os.path.join(caClientHomePath, "users", "AdminBankB@bankB.catena.id", "msp"),
                None,
                tlsCertFilePath)
    subprocess.run(["cp", 
        os.path.join(caClientHomePath, "msp", "config.yaml"),
        os.path.join(caClientHomePath, "users", "AdminBankB@bankB.catena.id", "msp", "config.yaml"),
    ])

    # Generating user1 MSP
    generateMsp("https://user1:user1pw@localhost:8054", "ca-bankBOrg",
                os.path.join(caClientHomePath, "users", "User1@bankB.catena.id", "msp"),
                None,
                tlsCertFilePath)
    subprocess.run(["cp", 
        os.path.join(caClientHomePath, "msp", "config.yaml"),
        os.path.join(caClientHomePath, "users", "User1@bankB.catena.id", "msp", "config.yaml"),
    ])

def createOrderer():
    caClientHomePath =  os.path.join(os.getcwd(), "organizations", "ordererOrganizations", "catena.id")
    os.makedirs(caClientHomePath)
    os.environ['FABRIC_CA_CLIENT_HOME'] = caClientHomePath

    tlsCertFilePath = os.path.join(os.getcwd(), "organizations", "fabric-ca", "ordererOrg", "tls-cert.pem")
    subprocess.run(["fabric-ca-client", "enroll", "-u", "https://admin:adminpw@localhost:9054",
                    "--caname", "ca-orderer", "--tls.certfiles", tlsCertFilePath])
    
    configYamlPath = os.path.join(os.getcwd(), caClientHomePath, "msp", "config.yaml")
    configNodeOUs = """NodeOUs:
  Enable: true
  ClientOUIdentifier:
    Certificate: cacerts/localhost-9054-ca-orderer.pem
    OrganizationalUnitIdentifier: client
  PeerOUIdentifier:
    Certificate: cacerts/localhost-9054-ca-orderer.pem
    OrganizationalUnitIdentifier: peer
  AdminOUIdentifier:
    Certificate: cacerts/localhost-9054-ca-orderer.pem
    OrganizationalUnitIdentifier: admin
  OrdererOUIdentifier:
    Certificate: cacerts/localhost-9054-ca-orderer.pem
    OrganizationalUnitIdentifier: orderer
    """

    # subprocess.run(["echo", configNodeOUs, ">", configYamlPath])
    configFile = open(configYamlPath, "w+")
    configFile.write(configNodeOUs)
    configFile.close()

    # Registering peer0
    registerCa("ca-orderer", "orderer", "ordererpw", "orderer", tlsCertFilePath)

    # Registering peer0
    registerCa("ca-orderer", "ordererAdmin", "ordererAdminpw", "admin", tlsCertFilePath)

    # Generate peer0 MSP
    subprocess.run(["fabric-ca-client", "enroll", "-u", "https://orderer:ordererpw@localhost:9054",
                    "--caname", "ca-orderer",
                    "-M", os.path.join(caClientHomePath, "orderers", "orderer.catena.id", "msp") ,
                    "--csr.hosts", "orderer.catena.id",
                    "--csr.hosts", "localhost",
                    "--tls.certfiles", tlsCertFilePath])
    subprocess.run(["cp", 
        os.path.join(caClientHomePath, "msp", "config.yaml"),
        os.path.join(caClientHomePath, "orderers", "orderer.catena.id", "msp", "config.yaml"),
    ])

    # Generate peer0 TLS Certificates
    generateTlsCert("https://orderer:ordererpw@localhost:9054", "ca-orderer",
                os.path.join(caClientHomePath, "orderers", "orderer.catena.id", "tls"),
                "tls",
                "orderer.catena.id",
                "localhost",
                tlsCertFilePath)
    
#    shutil.copyfile(
#         os.path.join(caClientHomePath, "peers", "peer0.bankA.catena.id", "tls", "tlscacerts"),
#    )

    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "orderers", "orderer.catena.id", "tls", "tlscacerts")),
        os.path.join(caClientHomePath, "orderers", "orderer.catena.id", "tls", "ca.crt"),
    ])

    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "orderers", "orderer.catena.id", "tls", "signcerts")),
        os.path.join(caClientHomePath, "orderers", "orderer.catena.id", "tls", "server.crt"),
    ])
    
    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "orderers", "orderer.catena.id", "tls", "keystore")),
        os.path.join(caClientHomePath, "orderers", "orderer.catena.id", "tls", "server.key"),
    ])

    os.makedirs(os.path.join(caClientHomePath, "orderers", "orderer.catena.id", "msp", "tlscacerts"))
    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "orderers", "orderer.catena.id", "tls", "tlscacerts")),
        os.path.join(caClientHomePath, "orderers", "orderer.catena.id", "msp", "tlscacerts", "tlsca.catena.id-cert.pem"),
    ])

    os.makedirs(os.path.join(caClientHomePath, "msp", "tlscacerts"))
    subprocess.run(["cp", 
        getFileFromDir(os.path.join(caClientHomePath, "orderers", "orderer.catena.id", "tls", "tlscacerts")),
        os.path.join(caClientHomePath, "msp", "tlscacerts", "tlsca.catena.id-cert.pem"),
    ])

    # Generating adminBankA MSP
    generateMsp("https://ordererAdmin:ordererAdminpw@localhost:9054", "ca-orderer",
                os.path.join(caClientHomePath, "users", "ordererAdmin@catena.id", "msp"),
                None,
                tlsCertFilePath)
    subprocess.run(["cp", 
        os.path.join(caClientHomePath, "msp", "config.yaml"),
        os.path.join(caClientHomePath, "users", "ordererAdmin@catena.id", "msp", "config.yaml"),
    ])

def registerCa(caName, idName, idSecret, idType, tlsCertfilePath):
    subprocess.run(["fabric-ca-client", "register", "--caname", caName,
                    "--id.name", idName, 
                    "--id.secret", idSecret,
                    "--id.type", idType,
                    "--tls.certfiles", tlsCertfilePath])

def generateMsp(u, caName, mPath, csrHosts, tlsCertFilePath):
    if csrHosts is None:
        subprocess.run(["fabric-ca-client", "enroll", "-u", u,
                        "--caname", caName,
                        "-M", mPath,
                        "--tls.certfiles", tlsCertFilePath])
    else:
        subprocess.run(["fabric-ca-client", "enroll", "-u", u,
                        "--caname", caName,
                        "-M", mPath,
                        "--csr.hosts", csrHosts,
                        "--tls.certfiles", tlsCertFilePath])

        
def generateTlsCert(u, caName, mPath, enrollmentProfile, csrHost1, csrHost2, tlsCertFilePath):
    subprocess.run(["fabric-ca-client", "enroll", "-u", u,
                    "--caname", caName,
                    "-M", mPath,
                    "--enrollment.profile", enrollmentProfile,
                    "--csr.hosts", csrHost1,
                    "--csr.hosts", csrHost2,
                    "--tls.certfiles", tlsCertFilePath])

def getFileFromDir(path):
    files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    return os.path.join(path, files[0])