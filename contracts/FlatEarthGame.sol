// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract FlatEarthGame is Ownable {
    IERC20 public gameToken;
    uint256 public constant GAME_PRICE = 100000000000000000; // 0.1 QUAI
    
    struct GameSession {
        bool active;
        uint256 startTime;
        bool completed;
    }
    
    mapping(address => GameSession) public gameSessions;
    mapping(address => bool) public payments;
    
    event GameStarted(address player, uint256 sessionId);
    event GameCompleted(address player, uint256 score, uint256 tokens);
    
    constructor(address _tokenAddress) {
        gameToken = IERC20(_tokenAddress);
    }
    
    function startGame() external payable {
        require(msg.value == GAME_PRICE, "Incorrect payment amount");
        require(!gameSessions[msg.sender].active, "Game already in progress");
        
        // Create new game session
        gameSessions[msg.sender] = GameSession({
            active: true,
            startTime: block.timestamp,
            completed: false
        });
        
        payments[msg.sender] = true;
        
        emit GameStarted(msg.sender, uint256(keccak256(abi.encodePacked(msg.sender, block.timestamp))));
    }
    
    function completeGame(address player, uint256 score) external onlyOwner {
        require(gameSessions[player].active, "No active game session");
        require(!gameSessions[player].completed, "Game already completed");
        
        // Calculate token reward (1 token per 10 points, max 100)
        uint256 tokenReward = (score / 10) > 100 ? 100 : (score / 10);
        
        // Mark game as completed
        gameSessions[player].completed = true;
        gameSessions[player].active = false;
        
        // Transfer tokens
        require(gameToken.transfer(player, tokenReward), "Token transfer failed");
        
        emit GameCompleted(player, score, tokenReward);
    }
    
    function checkPayment(address player) external view returns (bool) {
        return payments[player];
    }
    
    function getSessionId(address player) external view returns (uint256) {
        require(gameSessions[player].active, "No active game session");
        return uint256(keccak256(abi.encodePacked(player, gameSessions[player].startTime)));
    }
    
    // Allow owner to withdraw collected QUAI
    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}