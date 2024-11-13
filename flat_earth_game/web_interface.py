"""
Web interface for the Flat Earth Debate Game with Solana integration.
"""
from flask import Flask, request, jsonify
from .game import FlatEarthDebateGame
from .solana_integration import GameToken
import asyncio

app = Flask(__name__)
game_token = GameToken()

@app.route('/start_game', methods=['POST'])
async def start_game():
    """Start a new game session after payment verification"""
    data = request.json
    wallet_address = data.get('wallet_address')
    
    if not wallet_address:
        return jsonify({'error': 'Wallet address required'}), 400
        
    # Verify payment
    payment_verified = await game_token.verify_payment(wallet_address)
    if not payment_verified:
        return jsonify({
            'error': 'Payment required',
            'required_amount': 0.1,
            'wallet': str(game_token.game_wallet)
        }), 402
        
    # Create new game session
    game = FlatEarthDebateGame()
    session_id = str(hash(wallet_address + str(asyncio.get_event_loop().time())))
    
    return jsonify({
        'session_id': session_id,
        'message': 'Game started! Payment verified.'
    })

@app.route('/submit_argument', methods=['POST'])
async def submit_argument():
    """Handle player arguments and return game response"""
    data = request.json
    argument = data.get('argument')
    session_id = data.get('session_id')
    wallet_address = data.get('wallet_address')
    
    if not all([argument, session_id, wallet_address]):
        return jsonify({'error': 'Missing required data'}), 400
        
    game = FlatEarthDebateGame()  # In production, this would be stored in a session
    result = game.process_argument(argument)
    
    # If game is won, send token reward
    if result.get('state', {}).get('convinced', False):
        reward_sent = await game_token.reward_token(
            wallet_address,
            result['state']['credibility_score']
        )
        result['reward_sent'] = reward_sent
        
    return jsonify(result)

@app.route('/game_status', methods=['GET'])
def game_status():
    """Get current game status and token info"""
    return jsonify({
        'entry_fee': 0.1,
        'token_contract': str(game_token.token_mint),
        'payment_wallet': str(game_token.game_wallet)
    })

if __name__ == '__main__':
    app.run(debug=True)