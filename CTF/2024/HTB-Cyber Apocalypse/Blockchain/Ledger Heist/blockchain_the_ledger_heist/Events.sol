// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

interface Events {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event FlashLoanSuccessful(
        address indexed target, address indexed initiator, address indexed token, uint256 amount, uint256 fee
    );
    event FeesUpdated(address indexed token, address indexed user, uint256 fees);
}
