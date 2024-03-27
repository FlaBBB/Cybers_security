// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {LoanPool} from "./LoanPool.sol";
import {Token} from "./Token.sol";

contract Setup {
    LoanPool public immutable TARGET;
    Token public immutable TOKEN;

    constructor(address _user) {
        TOKEN = new Token(_user);
        TARGET = new LoanPool(address(TOKEN));

        TOKEN.approve(address(TARGET), type(uint256).max);
        TARGET.deposit(10 ether);
    }

    function isSolved() public view returns (bool) {
        return (TARGET.totalSupply() == 10 ether && TOKEN.balanceOf(address(TARGET)) < 10 ether);
    }
}
