"""Calculate Abu's estimated ELO rating from assessment results"""

import math


def calculate_elo_difference(score_percentage):
    """
    Calculate ELO difference from score percentage
    
    Args:
        score_percentage: Win rate as percentage (0-100)
    
    Returns:
        ELO difference (positive = Abu is stronger, negative = opponent is stronger)
    """
    # Convert percentage to probability
    score = score_percentage / 100.0
    
    # Avoid edge cases
    if score >= 0.99:
        score = 0.99
    elif score <= 0.01:
        score = 0.01
    
    # ELO formula: Difference = -400 * log10(1/score - 1)
    elo_diff = -400 * math.log10(1/score - 1)
    
    return elo_diff


def estimate_abu_elo(assessment1_score, assessment2_score, 
                     stockfish_depth=10, stockfish_noise=0.15):
    """
    Estimate Abu's ELO rating
    
    Args:
        assessment1_score: Score % vs Noisy Stockfish
        assessment2_score: Score % vs Normal Stockfish
        stockfish_depth: Stockfish search depth used
        stockfish_noise: Exploration noise in assessment 1
    
    Returns:
        Dictionary with ELO estimates
    """
    # Stockfish ELO estimates by depth (approximate)
    stockfish_elo_by_depth = {
        5: 1500,
        8: 2000,
        10: 2400,
        12: 2600,
        15: 2800,
        20: 3200
    }
    
    stockfish_elo = stockfish_elo_by_depth.get(stockfish_depth, 2400)
    
    # Noisy Stockfish is weaker (subtract ~200 ELO for 15% noise)
    noisy_stockfish_elo = stockfish_elo - int(stockfish_noise * 1000)
    
    # Calculate ELO differences
    elo_diff_1 = calculate_elo_difference(assessment1_score)
    elo_diff_2 = calculate_elo_difference(assessment2_score)
    
    # Estimate Abu's ELO
    abu_elo_1 = noisy_stockfish_elo + elo_diff_1
    abu_elo_2 = stockfish_elo + elo_diff_2
    
    # Average estimate
    abu_elo_avg = (abu_elo_1 + abu_elo_2) / 2
    
    return {
        'assessment1': {
            'opponent_elo': noisy_stockfish_elo,
            'score_pct': assessment1_score,
            'elo_diff': elo_diff_1,
            'abu_elo': abu_elo_1
        },
        'assessment2': {
            'opponent_elo': stockfish_elo,
            'score_pct': assessment2_score,
            'elo_diff': elo_diff_2,
            'abu_elo': abu_elo_2
        },
        'average_elo': abu_elo_avg,
        'elo_range': (min(abu_elo_1, abu_elo_2), max(abu_elo_1, abu_elo_2))
    }


def analyze_color_bias(white_score, black_score):
    """
    Analyze if Abu plays better as White or Black
    
    Args:
        white_score: Score % when playing as White
        black_score: Score % when playing as Black
    
    Returns:
        Analysis dictionary
    """
    diff = white_score - black_score
    
    if abs(diff) < 5:
        bias = "No significant color bias"
    elif diff > 0:
        bias = f"Plays {diff:.1f}% better as White"
    else:
        bias = f"Plays {abs(diff):.1f}% better as Black"
    
    return {
        'white_score': white_score,
        'black_score': black_score,
        'difference': diff,
        'bias': bias
    }


def main():
    print("=" * 70)
    print("ABU ELO CALCULATOR")
    print("=" * 70)
    print("\nEnter your assessment results to calculate Abu's ELO rating")
    print("=" * 70)
    
    # Get assessment results
    print("\nAssessment 1 (Abu vs Noisy Stockfish):")
    wins1 = int(input("  Wins: "))
    draws1 = int(input("  Draws: "))
    losses1 = int(input("  Losses: "))
    
    print("\nAssessment 2 (Abu vs Normal Stockfish):")
    wins2 = int(input("  Wins: "))
    draws2 = int(input("  Draws: "))
    losses2 = int(input("  Losses: "))
    
    # Optional: Color-specific analysis
    print("\n" + "=" * 70)
    color_analysis = input("Do you want color-specific analysis? (y/n): ").lower()
    
    if color_analysis == 'y':
        print("\nAssessment 1 - When Abu played White:")
        white_wins1 = int(input("  Wins: "))
        white_draws1 = int(input("  Draws: "))
        white_losses1 = int(input("  Losses: "))
        
        print("\nAssessment 1 - When Abu played Black:")
        black_wins1 = int(input("  Wins: "))
        black_draws1 = int(input("  Draws: "))
        black_losses1 = int(input("  Losses: "))
    
    # Calculate scores
    total1 = wins1 + draws1 + losses1
    total2 = wins2 + draws2 + losses2
    
    score1 = (wins1 + draws1 * 0.5) / total1 * 100
    score2 = (wins2 + draws2 * 0.5) / total2 * 100
    
    # Calculate ELO
    results = estimate_abu_elo(score1, score2)
    
    # Display results
    print("\n" + "=" * 70)
    print("ELO ESTIMATION RESULTS")
    print("=" * 70)
    
    print("\nAssessment 1 (vs Noisy Stockfish):")
    print(f"  Opponent ELO: {results['assessment1']['opponent_elo']:.0f}")
    print(f"  Abu's Score: {results['assessment1']['score_pct']:.1f}%")
    print(f"  ELO Difference: {results['assessment1']['elo_diff']:+.0f}")
    print(f"  Abu's Estimated ELO: {results['assessment1']['abu_elo']:.0f}")
    
    print("\nAssessment 2 (vs Normal Stockfish):")
    print(f"  Opponent ELO: {results['assessment2']['opponent_elo']:.0f}")
    print(f"  Abu's Score: {results['assessment2']['score_pct']:.1f}%")
    print(f"  ELO Difference: {results['assessment2']['elo_diff']:+.0f}")
    print(f"  Abu's Estimated ELO: {results['assessment2']['abu_elo']:.0f}")
    
    print("\n" + "=" * 70)
    print(f"ABU'S ESTIMATED ELO: {results['average_elo']:.0f}")
    print(f"ELO Range: {results['elo_range'][0]:.0f} - {results['elo_range'][1]:.0f}")
    print("=" * 70)
    
    # ELO interpretation
    elo = results['average_elo']
    if elo < 1000:
        level = "Beginner"
    elif elo < 1400:
        level = "Novice"
    elif elo < 1800:
        level = "Intermediate"
    elif elo < 2000:
        level = "Advanced"
    elif elo < 2200:
        level = "Expert"
    elif elo < 2400:
        level = "Master"
    else:
        level = "Grandmaster Level"
    
    print(f"\nSkill Level: {level}")
    
    # Color analysis
    if color_analysis == 'y':
        white_total = white_wins1 + white_draws1 + white_losses1
        black_total = black_wins1 + black_draws1 + black_losses1
        
        white_score = (white_wins1 + white_draws1 * 0.5) / white_total * 100
        black_score = (black_wins1 + black_draws1 * 0.5) / black_total * 100
        
        color_results = analyze_color_bias(white_score, black_score)
        
        print("\n" + "=" * 70)
        print("COLOR ANALYSIS")
        print("=" * 70)
        print(f"Score as White: {color_results['white_score']:.1f}%")
        print(f"Score as Black: {color_results['black_score']:.1f}%")
        print(f"Difference: {color_results['difference']:+.1f}%")
        print(f"\n{color_results['bias']}")
        print("=" * 70)
    
    print("\nNote: ELO estimates are approximate and based on limited games.")
    print("More games = more accurate rating!")


if __name__ == "__main__":
    main()
