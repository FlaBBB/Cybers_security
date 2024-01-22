import os

import solcx
from web3 import HTTPProvider, Web3

"""
https://github.com/foundry-rs/foundry

- Init new Project: forge init
- testing: forge test -vvv

UUID    ad59e825-def3-4f1f-8c03-2a759a3b89f6
RPC Endpoint    http://103.152.242.78:11661/ad59e825-def3-4f1f-8c03-2a759a3b89f6
Private Key     0x78f3efa9e3e79bf38b64e0ecd73a810e74724a9799d73abaaf9b9e9d0aba8c10
Setup Contract  0x9445d4FFb56eBCD64CFFa79Aab03edaE8B277318
Wallet  0xDd632e83c1FeA257F89C8B508030E013a870d659
"""

RPC_URL = "http://103.152.242.78:11661/ec67eaeb-e4ad-45c9-97fa-e2bd358327b1"
PRIVKEY = "0x4a5811b0794fcebb95024f9f8a1f5a47afc4cec253327c364e93268f016ece50"
SETUP_CONTRACT_ADDR = "0xC853b3f044f8621A2527Fca790C2ab9864c25575"

solcx.install_solc("0.8.0")
solcx.set_solc_version("0.8.0")


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
        super().__init__(
            addr=SETUP_CONTRACT_ADDR,
            file="./Setup.sol:Setup",
        )

    def target(self):
        return self.contract.functions.TARGET().call()

    def is_solved(s):
        result = s.contract.functions.isSolved().call()
        print("is solved:", result)


class ChallContract(BaseDeployedContract):
    def __init__(self, addr) -> None:
        super().__init__(addr, "./Chall.sol:Chall")

    def free_token(self):
        self.contract.functions.free_token().transact()

    def start(self, your_guess):
        self.contract.functions.start(your_guess).transact()

    def check_tokens(self):
        token = self.contract.functions.tokens(self.account_address).call()
        print("token:", token)


class HackContract(BaseUndeployedContract):
    def __init__(self) -> None:
        super().__init__("./Hack.sol:Hack")


if __name__ == "__main__":
    setup = SetupContract()
    target = setup.target()
    # print(target)
    chall = ChallContract(target)
    hack_base = HackContract()
    hack = hack_base.deploy_to_target(target)
    hack.contract.functions.hack().transact()
    setup.is_solved()
