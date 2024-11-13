"""
Web interface for the Flat Earth Debate Game with Quai Network integration.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from .game import FlatEarthDebateGame
from .quai_integration import QuaiGameContract

app = Flask(__name__)
CORS(app)  # Enable CORS for Pegasus wallet integration
quai = QuaiGameContract()

@app.route('/start_game', methods=['POST'])
def start_game():
    """Start a new game session after payment verification"""
    data = request.json
    wallet_address = data.get('wallet_address')
    
    if not wallet_address:
        return jsonify({'error': 'Wallet address required'}), 400
        
    # Verify payment and start game session
    result = quai.start_game_session(wallet_address)
    if not result['success']:
        return jsonify({
            'error': 'Payment required',
            'required_amount': 0.1,
            'contract_address': quai.game_address,
            'details': result.get('error', 'Payment failed')
        }), 402
        
    # Create new game session
    game = FlatEarthDebateGame()
    
    return jsonify({
        'session_id': result['session_id'],
        'transaction_hash': result['transaction_hash'],
        'message': 'Game started! Payment verified.'
    })

@app.route('/submit_argument', methods=['POST'])
def submit_argument():
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
        reward_result = quai.reward_winner(
            wallet_address,
            result['state']['credibility_score']
        )
        result['reward'] = reward_result
        
    return jsonify(result)

@app.route('/game_status', methods=['GET'])
def game_status():
    """Get current game status and token info"""
    return jsonify({
        'entry_fee': 0.1,
        'token_contract': quai.token_address,
        'game_contract': quai.game_address,
        'network': 'cyprus1.testnet.quai.network'
    })

@app.route('/token_balance/<address>', methods=['GET'])
def token_balance(address):
    """Get player's token balance"""
    balance = quai.get_player_token_balance(address)
    return jsonify({
        'address': address,
        'balance': balance,
        'token_contract': quai.token_address
    })

if __name__ == '__main__':
    app.run(debug=True)