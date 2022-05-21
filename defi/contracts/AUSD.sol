//SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
contract AUSD is ERC20{

    constructor() ERC20("AUSD", "AUSD"){
        _mint(msg.sender, 100000000000000000);
    }

}