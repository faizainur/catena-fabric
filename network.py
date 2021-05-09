import fire
import cagen as certgen
import subprocess
import os

COMPOSE_FILE_FABRIC = "docker/docker-compose-net.yaml"

def hello(name="World"):
    return "Hello %s" % name

def init():
    ca.initContainer()

def start(ca=False, fabric=False):
    if ca:
        print("Initiating Fabric CA...\n")
        certgen.initContainer()
    elif fabric:
        print("Initiating Fabric...\n")
        initFabricContainer()
        
def initFabricContainer():
    subprocess.run(["docker-compose", "-f", COMPOSE_FILE_FABRIC, "up", "-d"])
    subprocess.run(["docker", "ps"])

def cagen():
    print("======= Creating bankAOrg Identities =======")
    certgen.createBankAOrg()
    print("\n============================================")

    print("\n======= Creating bankBOrg Identities =======")
    certgen.createBankBOrg()
    print("\n============================================")

    # subprocess.run([""])
    subprocess.run(["./organizations/ccp-generate.sh"])

    print("\n======= Creating orderer Identities =======")
    certgen.createOrderer()

def dldep(verbose=False):
    if verbose == False:
        # Download and extract fabric binaries
        print("Downloading Fabric binaries...")
        subprocess.run(["wget", "-q", "https://github.com/hyperledger/fabric/releases/download/v2.3.2/hyperledger-fabric-linux-amd64-2.3.2.tar.gz"])
        print("Extracting Fabric binaries...")
        subprocess.run(["tar", "-xf", "hyperledger-fabric-linux-amd64-2.3.2.tar.gz"])

        # Download and extract Fabric CA binaries
        print("Downloading Fabric CA binaries...")
        subprocess.run(["wget", "-q", "https://github.com/hyperledger/fabric-ca/releases/download/v1.5.0/hyperledger-fabric-ca-linux-amd64-1.5.0.tar.gz"])
        print("Extracting Fabric CA binaries...")
        subprocess.run(["tar", "-xf", "hyperledger-fabric-ca-linux-amd64-1.5.0.tar.gz"])

        # Delete artifacts
        print("Deleting artifacts...")
        subprocess.run(["rm", "hyperledger-fabric-linux-amd64-2.3.2.tar.gz"])
        subprocess.run(["rm", "hyperledger-fabric-ca-linux-amd64-1.5.0.tar.gz"])

        print("\nAdd the binaries path to your PATH environment variables:") 
        print("\t", os.path.join(os.getcwd(), "bin"))
    else:
        # Download and extract fabric binaries
        print("Downloading Fabric binaries...")
        subprocess.run(["wget", "https://github.com/hyperledger/fabric/releases/download/v2.3.2/hyperledger-fabric-linux-amd64-2.3.2.tar.gz"])
        print("\nExtracting Fabric binaries...")
        subprocess.run(["tar", "-xvf", "hyperledger-fabric-linux-amd64-2.3.2.tar.gz"])

        # Download and extract Fabric CA binaries
        print("\nDownloading Fabric CA binaries...")
        subprocess.run(["wget", "https://github.com/hyperledger/fabric-ca/releases/download/v1.5.0/hyperledger-fabric-ca-linux-amd64-1.5.0.tar.gz"])
        print("\nExtracting Fabric CA binaries...")
        subprocess.run(["tar", "-xvf", "hyperledger-fabric-ca-linux-amd64-1.5.0.tar.gz"])

        # Delete artifacts
        print("\nDeleting artifacts...")
        subprocess.run(["rm", "hyperledger-fabric-linux-amd64-2.3.2.tar.gz"])
        subprocess.run(["rm", "hyperledger-fabric-ca-linux-amd64-1.5.0.tar.gz"])

        print("\nAdd the binaries path to your PATH environment variables:") 
        print("\t", os.path.join(os.getcwd(), "bin"))

def test(a=False, b=False):
    if a:
        print("Hello")
        # subprocess.run(["./organizations/ccp-generate.sh"])
    elif b:
        print("World")


if __name__ == '__main__':
    # ca.cagenHello()
    fire.Fire()