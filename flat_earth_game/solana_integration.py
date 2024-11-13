"""
Solana blockchain integration for the Flat Earth Debate Game.
"""
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solders.pubkey import Pubkey
import os
from dotenv import load_dotenv

class GameToken:
    """Manages the game's token operations"""
    def __init__(self):
        load_dotenv()
        self.client = AsyncClient(os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com"))
        self.game_wallet = Pubkey.from_string(os.getenv("GAME_WALLET"))
        self.token_mint = Pubkey.from_string(os.getenv("TOKEN_MINT"))
        
    async def verify_payment(self, player_wallet: str, amount: float = 0.1) -> bool:
        """
        Verify that a player has paid the required SOL
        
        Args:
            player_wallet: Player's Solana wallet address
            amount: Amount of SOL required (default 0.1)
            
        Returns:
            bool: True if payment verified, False otherwise
        """
        try:
            # Check recent transactions for payment
            player_pubkey = Pubkey.from_string(player_wallet)
            recent_txs = await self.client.get_signatures_for_address(player_pubkey)
            
            for tx in recent_txs.value:
                transaction = await self.client.get_transaction(tx.signature)
                # Verify transaction details
                if (transaction.value and 
                    transaction.value.transaction.message.recent_blockhash and
                    transaction.value.transaction.signatures):
                    # Check if transaction is a transfer to game wallet
                    for ix in transaction.value.transaction.message.instructions:
                        if (ix.program_id == self.game_wallet and 
                            ix.data.amount == amount * 10**9):  # Convert to lamports
                            return True
            return False
        except Exception as e:
            print(f"Error verifying payment: {e}")
            return False
            
    async def reward_token(self, player_wallet: str, score: int) -> bool:
        """
        Reward player with tokens based on their game performance
        
        Args:
            player_wallet: Player's Solana wallet address
            score: Player's final game score
            
        Returns:
            bool: True if tokens were successfully sent
        """
        try:
            # Calculate token reward based on score
            token_amount = min(score // 10, 100)  # Max 100 tokens
            
            # Create token transfer instruction
            player_pubkey = Pubkey.from_string(player_wallet)
            transfer_ix = transfer(
                TransferParams(
                    from_pubkey=self.game_wallet,
                    to_pubkey=player_pubkey,
                    lamports=token_amount * 10**9  # Convert to smallest unit
                )
            )
            
            # Create and send transaction
            transaction = Transaction().add(transfer_ix)
            result = await self.client.send_transaction(transaction)
            
            return "result" in result and result["result"]
        except Exception as e:
            print(f"Error sending reward tokens: {e}")
            return False