#!/usr/bin/env python3
"""
Fix Cumulative Tracker Results

Updates incorrect match results in the cumulative picks tracker
"""

import pandas as pd
import numpy as np

def fix_cape_verde_cameroon():
    """Fix the Cape Verde vs Cameroon result"""
    
    tracker_file = "/Users/richardgibbons/soccer betting python/soccer/output reports/cumulative_picks_tracker.csv"
    
    print("🔧 Fixing Cape Verde vs Cameroon result...")
    print("❌ Incorrect: Cape Verde 3-0 Cameroon (Over 1.5 Goals = Win)")  
    print("✅ Correct: Cameroon 1-0 Cape Verde (Over 1.5 Goals = Loss)")
    
    # Load the tracker
    df = pd.read_csv(tracker_file)
    
    # Find the Cape Verde vs Cameroon match
    cape_verde_mask = (df['home_team'] == 'Cape Verde Islands') & (df['away_team'] == 'Cameroon')
    
    if cape_verde_mask.any():
        row_index = df[cape_verde_mask].index[0]
        print(f"📍 Found match at row {row_index + 2} (CSV line {row_index + 2})")
        
        # Show current incorrect data
        current_row = df.loc[row_index]
        print(f"Current: {current_row['home_team']} {current_row['home_score']}-{current_row['away_score']} {current_row['away_team']}")
        print(f"Bet: {current_row['bet_description']}")
        print(f"Current outcome: {current_row['bet_outcome']} (P&L: ${current_row['actual_pnl']})")
        
        # Update with correct result: Cameroon 1-0 Cape Verde  
        df.loc[row_index, 'home_score'] = 0  # Cape Verde scored 0
        df.loc[row_index, 'away_score'] = 1  # Cameroon scored 1
        df.loc[row_index, 'total_goals'] = 1  # 1 total goal
        df.loc[row_index, 'btts'] = False    # Only Cameroon scored
        
        # Over 1.5 Goals with 1 total goal = Loss
        df.loc[row_index, 'bet_outcome'] = 'Loss'
        df.loc[row_index, 'actual_pnl'] = -25.0  # Lost $25
        
        print(f"✅ Updated: Cape Verde 0-1 Cameroon")
        print(f"✅ Over 1.5 Goals = Loss (only 1 goal scored)")
        print(f"✅ P&L: -$25.00")
        
        # Now recalculate running totals for all subsequent rows
        print("🔄 Recalculating running totals...")
        
        # Get the running total from the previous row
        if row_index > 0:
            previous_total = df.loc[row_index - 1, 'running_total']
        else:
            previous_total = 0
        
        # Update running totals from this row forward
        for i in range(row_index, len(df)):
            if i == row_index:
                # This row: start from previous total + current P&L
                df.loc[i, 'running_total'] = previous_total + df.loc[i, 'actual_pnl']
            else:
                # Subsequent rows: add their P&L to running total
                df.loc[i, 'running_total'] = df.loc[i-1, 'running_total'] + df.loc[i, 'actual_pnl']
            
            # Recalculate win rate
            total_picks = i + 1
            wins_so_far = len(df[:i+1][df[:i+1]['bet_outcome'] == 'Win'])
            win_rate = (wins_so_far / total_picks) * 100
            df.loc[i, 'win_rate'] = win_rate
        
        # Save the corrected tracker
        df.to_csv(tracker_file, index=False)
        
        # Show final statistics
        final_row = df.iloc[-1]
        total_picks = len(df)
        total_wins = len(df[df['bet_outcome'] == 'Win'])
        total_losses = len(df[df['bet_outcome'] == 'Loss'])
        final_total = final_row['running_total']
        final_win_rate = final_row['win_rate']
        
        print(f"\n📊 Updated Tracker Statistics:")
        print(f"   🎯 Total Picks: {total_picks}")
        print(f"   ✅ Wins: {total_wins}")
        print(f"   ❌ Losses: {total_losses}")
        print(f"   💰 Final P&L: ${final_total:+.2f}")
        print(f"   📈 Win Rate: {final_win_rate:.1f}%")
        print(f"   💾 Tracker updated: {tracker_file}")
        
        return True
    else:
        print("❌ Cape Verde vs Cameroon match not found in tracker")
        return False

if __name__ == "__main__":
    fix_cape_verde_cameroon()