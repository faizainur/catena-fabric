import fire
import cagen as ca
import subprocess
import os

def hello(name="World"):
    return "Hello %s" % name

def init():
    ca.initContainer()

def cagen():
    print("======= Creating bankAOrg Identities =======")
    ca.createBankAOrg()
    print("\n============================================")

    print("\n======= Creating bankBOrg Identities =======")
    ca.createBankBOrg()
    print("\n============================================")

    print("\n======= Creating orderer Identities =======")
    ca.createOrderer()

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


if __name__ == '__main__':
    # ca.cagenHello()
    fire.Fire()