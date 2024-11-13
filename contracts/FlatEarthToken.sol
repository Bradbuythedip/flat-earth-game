// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract FlatEarthToken is ERC20, Ownable {
    constructor() ERC20("Flat Earth Debate Token", "FLAT") {
        // Mint initial supply to contract creator
        _mint(msg.sender, 1000000 * 10 ** decimals()); // 1 million tokens
    }
    
    // Allow game contract to mint tokens for rewards
    function mintReward(address to, uint256 amount) external onlyOwner {
        _mint(to, amount * 10 ** decimals());
    }
}