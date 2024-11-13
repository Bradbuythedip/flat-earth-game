"""
Quai Network integration for the Flat Earth Debate Game.
"""
from web3 import Web3
import json
import os
from dotenv import load_dotenv

class QuaiGameContract:
    """Manages the game's blockchain operations on Quai Network"""
    
    def __init__(self):
        load_dotenv()
        # Quai Testnet Cyprus-1 Zone RPC
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('QUAI_RPC_URL', 'https://rpc.cyprus1.testnet.quai.network')))
        self.game_address = os.getenv('GAME_CONTRACT_ADDRESS')
        self.token_address = os.getenv('TOKEN_CONTRACT_ADDRESS')
        
        # Load contract ABIs
        with open('contracts/GameABI.json', 'r') as f:
            self.game_abi = json.load(f)
        with open('contracts/TokenABI.json', 'r') as f:
            self.token_abi = json.load(f)
            
        # Initialize contract instances
        self.game_contract = self.w3.eth.contract(
            address=self.game_address,
            abi=self.game_abi
        )
        self.token_contract = self.w3.eth.contract(
            address=self.token_address,
            abi=self.token_abi
        )
        
    def verify_payment(self, player_address: str) -> bool:
        """
        Verify that a player has paid the required QUAI
        
        Args:
            player_address: Player's Quai wallet address
            
        Returns:
            bool: True if payment verified
        """
        try:
            required_amount = self.w3.to_wei(0.1, 'ether')  # 0.1 QUAI
            payment_status = self.game_contract.functions.checkPayment(
                player_address
            ).call()
            return payment_status
        except Exception as e:
            print(f"Error verifying payment: {e}")
            return False
            
    def start_game_session(self, player_address: str) -> dict:
        """
        Start a new game session
        
        Args:
            player_address: Player's Quai wallet address
            
        Returns:
            dict: Session information
        """
        try:
            tx_hash = self.game_contract.functions.startGame().transact({
                'from': player_address,
                'value': self.w3.to_wei(0.1, 'ether')
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            session_id = self.game_contract.functions.getSessionId(
                player_address
            ).call()
            return {
                'success': True,
                'session_id': session_id,
                'transaction_hash': receipt['transactionHash'].hex()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def reward_winner(self, player_address: str, score: int) -> dict:
        """
        Send token rewards to winning player
        
        Args:
            player_address: Player's Quai wallet address
            score: Final game score
            
        Returns:
            dict: Reward transaction details
        """
        try:
            # Calculate token reward (1 token per 10 points, max 100)
            token_amount = min(score // 10, 100)
            tx_hash = self.game_contract.functions.rewardPlayer(
                player_address,
                token_amount
            ).transact()
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return {
                'success': True,
                'tokens_sent': token_amount,
                'transaction_hash': receipt['transactionHash'].hex()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def get_player_token_balance(self, player_address: str) -> int:
        """
        Get player's game token balance
        
        Args:
            player_address: Player's Quai wallet address
            
        Returns:
            int: Token balance
        """
        try:
            balance = self.token_contract.functions.balanceOf(
                player_address
            ).call()
            return balance
        except Exception as e:
            print(f"Error getting token balance: {e}")
            return 0