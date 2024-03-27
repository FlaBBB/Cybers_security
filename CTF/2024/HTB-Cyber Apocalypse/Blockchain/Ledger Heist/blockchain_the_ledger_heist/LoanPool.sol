// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {FixedMathLib} from "./FixedPointMath.sol";
import "./Errors.sol";
import {IERC20Minimal, IERC3156FlashBorrower} from "./Interfaces.sol";
import {Events} from "./Events.sol";

struct UserRecord {
    uint256 feePerShare;
    uint256 fees;
    uint256 balance;
}

contract LoanPool is Events {
    using FixedMathLib for uint256;

    uint256 constant BONE = 10 ** 18;

    address public underlying;
    uint256 public totalSupply;
    uint256 public feePerShare;
    mapping(address => UserRecord) public userRecords;

    constructor(address _underlying) {
        underlying = _underlying;
    }

    function deposit(uint256 amount) external {
        address _msgsender = msg.sender;

        _updateFees(_msgsender);
        IERC20Minimal(underlying).transferFrom(_msgsender, address(this), amount);

        _mint(_msgsender, amount);
    }

    function withdraw(uint256 amount) external {
        address _msgsender = msg.sender;

        if (userRecords[_msgsender].balance < amount) {
            revert InsufficientBalance();
        }

        _updateFees(_msgsender);
        _burn(_msgsender, amount);

        // Send also any fees accumulated to user
        uint256 fees = userRecords[_msgsender].fees;
        if (fees > 0) {
            userRecords[_msgsender].fees = 0;
            amount += fees;
            emit FeesUpdated(underlying, _msgsender, fees);
        }

        IERC20Minimal(underlying).transfer(_msgsender, amount);
    }

    function balanceOf(address account) public view returns (uint256) {
        return userRecords[account].balance;
    }

    // Flash loan EIP
    function maxFlashLoan(address token) external view returns (uint256) {
        if (token != underlying) {
            revert NotSupported(token);
        }
        return IERC20Minimal(token).balanceOf(address(this));
    }

    function flashFee(address token, uint256 amount) external view returns (uint256) {
        if (token != underlying) {
            revert NotSupported(token);
        }
        return _computeFee(amount);
    }

    function flashLoan(IERC3156FlashBorrower receiver, address token, uint256 amount, bytes calldata data)
        external
        returns (bool)
    {
        if (token != underlying) {
            revert NotSupported(token);
        }

        IERC20Minimal _token = IERC20Minimal(underlying);
        uint256 _balanceBefore = _token.balanceOf(address(this));

        if (amount > _balanceBefore) {
            revert InsufficientBalance();
        }

        uint256 _fee = _computeFee(amount);
        _token.transfer(address(receiver), amount);

        if (
            receiver.onFlashLoan(msg.sender, underlying, amount, _fee, data)
                != keccak256("ERC3156FlashBorrower.onFlashLoan")
        ) {
            revert CallbackFailed();
        }

        uint256 _balanceAfter = _token.balanceOf(address(this));
        if (_balanceAfter < _balanceBefore + _fee) {
            revert LoanNotRepaid();
        }

        // Accumulate fees and update feePerShare
        uint256 interest = _balanceAfter - _balanceBefore;
        feePerShare += interest.fixedDivFloor(totalSupply, BONE);

        emit FlashLoanSuccessful(address(receiver), msg.sender, token, amount, _fee);
        return true;
    }

    // Private methods
    function _mint(address to, uint256 amount) private {
        totalSupply += amount;
        userRecords[to].balance += amount;

        emit Transfer(address(0), to, amount);
    }

    function _burn(address from, uint256 amount) private {
        totalSupply -= amount;
        userRecords[from].balance -= amount;

        emit Transfer(from, address(0), amount);
    }

    function _updateFees(address _user) private {
        UserRecord storage record = userRecords[_user];
        uint256 fees = record.balance.fixedMulCeil((feePerShare - record.feePerShare), BONE);

        record.fees += fees;
        record.feePerShare = feePerShare;

        emit FeesUpdated(underlying, _user, fees);
    }

    function _computeFee(uint256 amount) private pure returns (uint256) {
        // 0.05% fee
        return amount.fixedMulCeil(5 * BONE / 10_000, BONE);
    }
}
