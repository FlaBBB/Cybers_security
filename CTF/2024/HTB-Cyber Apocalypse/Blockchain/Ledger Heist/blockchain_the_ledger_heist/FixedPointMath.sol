// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

library FixedMathLib {
    function fixedMulFloor(uint256 self, uint256 b, uint256 denominator) internal pure returns (uint256) {
        return self * b / denominator;
    }

    function fixedMulCeil(uint256 self, uint256 b, uint256 denominator) internal pure returns (uint256 result) {
        uint256 _mul = self * b;
        if (_mul % denominator == 0) {
            result = _mul / denominator;
        } else {
            result = _mul / denominator + 1;
        }
    }

    function fixedDivFloor(uint256 self, uint256 b, uint256 denominator) internal pure returns (uint256) {
        return self * denominator / b;
    }

    function fixedDivCeil(uint256 self, uint256 b, uint256 denominator) internal pure returns (uint256 result) {
        uint256 _mul = self * denominator;
        if (_mul % b == 0) {
            result = _mul / b;
        } else {
            result = _mul / b + 1;
        }
    }
}
