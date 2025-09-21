#!/usr/bin/env python3
"""
Leagues and Season ID Report Generator
Generates comprehensive report of all leagues we follow and their season IDs
"""

import pandas as pd
import csv
from datetime import datetime

def generate_leagues_season_report():
    """Generate comprehensive report of all followed leagues and their season IDs"""
    
    print("📋 GENERATING LEAGUES & SEASON ID REPORT")
    print("=" * 50)
    
    # Read the supported leagues database
    leagues_file = "/Users/richardgibbons/soccer betting python/soccer/output reports/UPDATED_supported_leagues_database.csv"
    
    try:
        # Read the CSV file
        df = pd.read_csv(leagues_file)
        
        print(f"📊 Found {len(df)} leagues in database")
        
        # Generate timestamp for report files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create detailed report
        report_filename = f"/Users/richardgibbons/soccer betting python/soccer/output reports/leagues_season_id_report_{timestamp}.txt"
        
        with open(report_filename, 'w') as f:
            f.write("⚽ FOLLOWED LEAGUES & SEASON ID REPORT ⚽\n")
            f.write("=" * 55 + "\n")
            f.write(f"📅 Generated: {datetime.now().strftime('%A, %B %d, %Y at %H:%M')}\n")
            f.write(f"📊 Total Leagues: {len(df)}\n\n")
            
            # Summary statistics
            active_leagues = len(df[df['status'] == 'Active'])
            need_id_leagues = len(df[df['status'] == 'ID Needed'])
            
            f.write("📈 STATUS SUMMARY:\n")
            f.write("-" * 20 + "\n")
            f.write(f"   🟢 Active Leagues: {active_leagues}\n")
            f.write(f"   🔴 Need Season ID: {need_id_leagues}\n")
            f.write(f"   📊 Total Coverage: {len(df)} leagues\n\n")
            
            # Group by status
            f.write("🟢 ACTIVE LEAGUES (Season ID Configured):\n")
            f.write("=" * 45 + "\n\n")
            
            active_df = df[df['status'] == 'Active'].sort_values(['country', 'tier', 'league_name'])
            
            current_country = ""
            for _, league in active_df.iterrows():
                if league['country'] != current_country:
                    current_country = league['country']
                    f.write(f"🌍 {current_country}:\n")
                
                tier_text = f"Tier {league['tier']}" if league['tier'] > 0 else "Continental/International"
                f.write(f"   ✅ {league['league_name']}\n")
                f.write(f"      🆔 League ID: {league['league_id']}\n")
                f.write(f"      📅 Season: {league['current_season']}\n")
                f.write(f"      🏆 {tier_text}\n")
                f.write(f"      📊 Betting Factors: {league['betting_factors_configured']}\n\n")
            
            f.write("🔴 LEAGUES NEEDING SEASON IDs:\n")
            f.write("=" * 35 + "\n\n")
            
            need_id_df = df[df['status'] == 'ID Needed'].sort_values(['country', 'tier', 'league_name'])
            
            current_country = ""
            for _, league in need_id_df.iterrows():
                if league['country'] != current_country:
                    current_country = league['country']
                    f.write(f"🌍 {current_country}:\n")
                
                tier_text = f"Tier {league['tier']}" if league['tier'] > 0 else "Continental/International"
                f.write(f"   ❌ {league['league_name']}\n")
                f.write(f"      🆔 League ID: {league['league_id']}\n")
                f.write(f"      📅 Season: {league['current_season']}\n")
                f.write(f"      🏆 {tier_text}\n")
                f.write(f"      ⚠️ Status: Season ID Required\n\n")
            
            # Regional breakdown
            f.write("🌍 REGIONAL BREAKDOWN:\n")
            f.write("=" * 25 + "\n\n")
            
            regional_stats = df.groupby('country').agg({
                'league_name': 'count',
                'status': lambda x: (x == 'Active').sum()
            }).rename(columns={'league_name': 'total_leagues', 'status': 'active_leagues'})
            
            regional_stats = regional_stats.sort_values('total_leagues', ascending=False)
            
            for country, stats in regional_stats.iterrows():
                active_count = int(stats['active_leagues'])
                total_count = int(stats['total_leagues'])
                coverage_pct = (active_count / total_count * 100) if total_count > 0 else 0
                
                f.write(f"📍 {country}:\n")
                f.write(f"   📊 {total_count} leagues, {active_count} active ({coverage_pct:.1f}%)\n")
                
                # List leagues for this country
                country_leagues = df[df['country'] == country].sort_values(['tier', 'league_name'])
                for _, league in country_leagues.iterrows():
                    status_icon = "🟢" if league['status'] == 'Active' else "🔴"
                    tier_text = f"T{league['tier']}" if league['tier'] > 0 else "Int'l"
                    f.write(f"      {status_icon} {league['league_name']} (ID: {league['league_id']}, {tier_text})\n")
                f.write("\n")
            
            # Tier breakdown
            f.write("🏆 TIER BREAKDOWN:\n")
            f.write("=" * 20 + "\n\n")
            
            tier_stats = df.groupby('tier').agg({
                'league_name': 'count',
                'status': lambda x: (x == 'Active').sum()
            }).rename(columns={'league_name': 'total_leagues', 'status': 'active_leagues'})
            
            tier_names = {
                0: "Continental/International",
                1: "Top Tier (1st Division)",
                2: "Second Tier (2nd Division)", 
                3: "Third Tier (3rd Division)"
            }
            
            for tier, stats in tier_stats.iterrows():
                tier_name = tier_names.get(tier, f"Tier {tier}")
                active_count = int(stats['active_leagues'])
                total_count = int(stats['total_leagues'])
                
                f.write(f"🎖️ {tier_name}:\n")
                f.write(f"   📊 {total_count} leagues, {active_count} active\n")
                
                # List leagues for this tier
                tier_leagues = df[df['tier'] == tier].sort_values(['country', 'league_name'])
                for _, league in tier_leagues.iterrows():
                    status_icon = "🟢" if league['status'] == 'Active' else "🔴"
                    f.write(f"      {status_icon} {league['league_name']} ({league['country']}, ID: {league['league_id']})\n")
                f.write("\n")
            
            f.write("⚠️ IMPORTANT NOTES:\n")
            f.write("• 🟢 Active = League has working season ID and is generating picks\n")
            f.write("• 🔴 ID Needed = League configured but needs current season ID\n")
            f.write("• Tier 0 = Continental competitions (Champions League, etc.)\n")
            f.write("• Tier 1 = Top domestic leagues (Premier League, etc.)\n")
            f.write("• Tier 2+ = Lower division leagues\n")
            f.write("• All leagues have betting factors configured\n")
            f.write("• Season formats vary by region (2025 vs 2025-26)\n")
        
        print(f"📋 Leagues report saved: leagues_season_id_report_{timestamp}.txt")
        
        # Also create a simplified CSV for easy reference
        csv_filename = f"/Users/richardgibbons/soccer betting python/soccer/output reports/leagues_summary_{timestamp}.csv"
        
        # Create summary data
        summary_data = []
        for _, league in df.iterrows():
            summary_data.append({
                'league_name': league['league_name'],
                'country': league['country'],
                'league_id': league['league_id'],
                'current_season': league['current_season'],
                'status': league['status'],
                'tier': league['tier']
            })
        
        # Save summary CSV
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['league_name', 'country', 'league_id', 'current_season', 'status', 'tier']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in summary_data:
                writer.writerow(row)
        
        print(f"💾 Summary CSV saved: leagues_summary_{timestamp}.csv")
        
        # Print summary to console
        print(f"\n📊 LEAGUE COVERAGE SUMMARY:")
        print(f"   🟢 Active Leagues: {active_leagues}")
        print(f"   🔴 Need Season ID: {need_id_leagues}")
        print(f"   📈 Coverage Rate: {active_leagues}/{len(df)} ({active_leagues/len(df)*100:.1f}%)")
        
        print(f"\n🌍 TOP REGIONS:")
        top_regions = regional_stats.head(5)
        for country, stats in top_regions.iterrows():
            print(f"   {country}: {int(stats['total_leagues'])} leagues ({int(stats['active_leagues'])} active)")
        
        return df
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find leagues database file: {leagues_file}")
        return None
    except Exception as e:
        print(f"❌ Error reading leagues database: {e}")
        return None


def main():
    """Generate leagues and season ID report"""
    
    print("📋 Starting Leagues & Season ID Report Generation...")
    
    leagues_df = generate_leagues_season_report()
    
    if leagues_df is not None:
        print(f"\n✅ Leagues & Season ID Report Generated Successfully!")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"📁 Files created:")
        print(f"   • leagues_season_id_report_{timestamp}.txt")
        print(f"   • leagues_summary_{timestamp}.csv")
    else:
        print("❌ Failed to generate report")


if __name__ == "__main__":
    main()