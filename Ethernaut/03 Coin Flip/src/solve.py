import os

import solcx
from web3 import HTTPProvider, Web3

RPC_URL = "https://sepolia.infura.io/v3/6f4f2ff82d1f425db50c084fefb52235"
PRIVKEY = "0xdc9086c1e50bd7786f6f057465acc02acd23f9dd9dacef124f22bcd035a25471"
CHALL_CONTRACT_ADDR = "0x7c50611C295042Da03c2168563F4c42c27107b48"

solcx.install_solc("0.8.0")
solcx.set_solc_version("0.8.0")


class Account:
    def __init__(self) -> None:
        self.w3 = Web3(HTTPProvider(RPC_URL))
        self.w3.eth.default_account = self.w3.eth.account.from_key(PRIVKEY).address
        self.account_address = self.w3.eth.default_account

    def get_balance(s, addr):
        print(f"balance {addr}:", s.w3.eth.get_balance(addr))


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
        nonce = self.w3.eth.get_transaction_count(self.w3.eth.default_account)
        gas_price = self.w3.eth.gas_price
        gas_estimate = self.contract.constructor(target).estimate_gas()
        txn = self.contract.constructor(target).build_transaction(
            {"nonce": nonce, "gas": gas_estimate, "gasPrice": gas_price}
        )
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=PRIVKEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=600)
        print(self.path, "deployed to", tx_receipt["contractAddress"])
        return BaseDeployedContract(tx_receipt["contractAddress"], self.path)


class CoinFlipContract(BaseDeployedContract):
    def __init__(self, addr) -> None:
        super().__init__(addr, "/Chall.sol:CoinFlip")

    def flip(self):
        nonce = self.w3.eth.get_transaction_count(self.w3.eth.default_account)
        gas_price = self.w3.eth.gas_price
        gas_estimate = self.contract.functions.flip().estimate_gas()
        txn = self.contract.functions.flip().build_transaction(
            {"nonce": nonce, "gas": gas_estimate, "gasPrice": gas_price}
        )
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=PRIVKEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt


class HackContractUndeploy(BaseUndeployedContract):
    def __init__(self) -> None:
        super().__init__("./Hack.sol:Hack")


class HackContract(BaseDeployedContract):
    def __init__(self, addr) -> None:
        super().__init__(addr, "./Hack.sol:Hack")

    def attack(self):
        nonce = self.w3.eth.get_transaction_count(self.w3.eth.default_account)
        gas_price = self.w3.eth.gas_price
        gas_estimate = self.contract.functions.attack().estimate_gas()
        txn = self.contract.functions.attack().build_transaction(
            {"nonce": nonce, "gas": gas_estimate, "gasPrice": gas_price}
        )
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=PRIVKEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def hack(self):
        nonce = self.w3.eth.get_transaction_count(self.w3.eth.default_account)
        gas_price = self.w3.eth.gas_price
        gas_estimate = self.contract.functions.hack().estimate_gas()
        txn = self.contract.functions.hack().build_transaction(
            {"nonce": nonce, "gas": gas_estimate, "gasPrice": gas_price}
        )
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=PRIVKEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=600)
        return tx_receipt


if __name__ == "__main__":
    # hack_base = HackContractUndeploy()
    # hack = hack_base.deploy_to_target(CHALL_CONTRACT_ADDR)
    # nonce = hack.w3.eth.get_transaction_count(hack.w3.eth.default_account)
    # gas_price = hack.w3.eth.gas_price
    # gas_estimate = hack.contract.functions.hack().estimate_gas()
    # txn = hack.contract.functions.hack().build_transaction(
    #     {"nonce": nonce, "gas": gas_estimate, "gasPrice": gas_price}
    # )
    # signed_txn = hack.w3.eth.account.sign_transaction(txn, private_key=PRIVKEY)
    # tx_hash = hack.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # res = hack.w3.eth.wait_for_transaction_receipt(tx_hash)

    hack_base = HackContract("0x609DAf0747bE916213d2134C89a8BE1AbF75bF17")
    for _ in range(10):
        hack_base.hack()