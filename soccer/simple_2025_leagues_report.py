#!/usr/bin/env python3
"""
Simple 2025 Leagues Report Generator
Shows all leagues we follow with complete 2025 league and season ID information
"""

import pandas as pd
import csv
from datetime import datetime

def generate_simple_2025_report():
    """Generate simple comprehensive report of all 2025 leagues with IDs"""
    
    print("📋 GENERATING 2025 LEAGUES & IDS REPORT")
    print("=" * 45)
    
    # Read the 2025 comprehensive league data
    leagues_2025_file = "/Users/richardgibbons/soccer betting python/soccer/output reports/all_leagues_2025_season_ids.csv"
    
    try:
        df = pd.read_csv(leagues_2025_file)
        print(f"📊 Found {len(df)} leagues in 2025 database")
        
        # Generate timestamp for report files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create comprehensive report
        report_filename = f"/Users/richardgibbons/soccer betting python/soccer/output reports/all_2025_leagues_with_ids_{timestamp}.txt"
        
        with open(report_filename, 'w') as f:
            f.write("⚽ ALL FOLLOWED LEAGUES WITH 2025 SEASON IDs ⚽\n")
            f.write("=" * 55 + "\n")
            f.write(f"📅 Generated: {datetime.now().strftime('%A, %B %d, %Y at %H:%M')}\n")
            f.write(f"📊 Total Leagues: {len(df)}\n\n")
            
            # Summary statistics
            confirmed_leagues = len(df[df['status'] == 'Confirmed'])
            estimated_leagues = len(df[df['status'] == 'Estimated'])
            total_matches = df['estimated_matches'].sum()
            
            f.write("📈 SUMMARY STATISTICS:\n")
            f.write("-" * 25 + "\n")
            f.write(f"   ✅ Confirmed Season IDs: {confirmed_leagues}\n")
            f.write(f"   📋 Estimated Season IDs: {estimated_leagues}\n")
            f.write(f"   ⚽ Total Estimated Matches: {total_matches:,}\n")
            f.write(f"   🌍 Countries Covered: {df['country'].nunique()}\n\n")
            
            # Group by region for detailed listing
            f.write("🌍 ALL LEAGUES BY REGION:\n")
            f.write("=" * 30 + "\n\n")
            
            regions = df.groupby('country').size().sort_values(ascending=False)
            
            for country, count in regions.items():
                country_leagues = df[df['country'] == country].sort_values(['tier', 'league_name'])
                
                f.write(f"📍 {country.upper()} ({count} leagues):\n")
                f.write("-" * (len(country) + 15) + "\n")
                
                for _, league in country_leagues.iterrows():
                    tier_text = f"Tier {league['tier']}" if league['tier'] > 0 else "Cup/Continental"
                    status_icon = "✅" if league['status'] == 'Confirmed' else "📋"
                    
                    f.write(f"   {status_icon} {league['league_name']:<35}\n")
                    f.write(f"      🆔 Season ID: {league['season_id']:<6} | Season: {league['season_year']}\n")
                    f.write(f"      🏆 {tier_text:<15} | Period: {league['typical_start']}-{league['typical_end']}\n")
                    f.write(f"      ⚽ Est. Matches: {league['estimated_matches']:<4} | Markets: {league['betting_markets_available']}\n\n")
                
                f.write("\n")
            
            f.write("🏆 LEAGUES BY TIER:\n")
            f.write("=" * 20 + "\n\n")
            
            tier_groups = df.groupby('tier')
            tier_names = {
                0: "🏆 CUPS & CONTINENTAL COMPETITIONS",
                1: "🥇 TOP TIER (1st Division)",
                2: "🥈 SECOND TIER (2nd Division)",
                3: "🥉 THIRD TIER (3rd Division)",
                4: "4️⃣ FOURTH TIER (4th Division)",
                5: "5️⃣ FIFTH TIER (5th Division)"
            }
            
            for tier, group in tier_groups:
                tier_name = tier_names.get(tier, f"Tier {tier}")
                confirmed_count = len(group[group['status'] == 'Confirmed'])
                f.write(f"{tier_name} ({len(group)} leagues, {confirmed_count} confirmed):\n")
                f.write("-" * 60 + "\n")
                
                for _, league in group.sort_values(['country', 'league_name']).iterrows():
                    status_icon = "✅" if league['status'] == 'Confirmed' else "📋"
                    f.write(f"   {status_icon} {league['league_name']:<30} ({league['country']:<12}) ID: {league['season_id']:<6}\n")
                
                f.write("\n")
            
            # Most active leagues
            f.write("📊 TOP 20 MOST ACTIVE LEAGUES (By Estimated Matches):\n")
            f.write("=" * 55 + "\n\n")
            
            top_active = df.nlargest(20, 'estimated_matches')
            for i, (_, league) in enumerate(top_active.iterrows(), 1):
                status_icon = "✅" if league['status'] == 'Confirmed' else "📋"
                f.write(f"{i:2}. {status_icon} {league['league_name']:<30} {league['estimated_matches']:3} matches\n")
                f.write(f"     🌍 {league['country']:<15} 🆔 ID: {league['season_id']:<6} 📅 {league['season_year']}\n\n")
            
            f.write("✅ CONFIRMED 2025 SEASON IDs:\n")
            f.write("=" * 35 + "\n\n")
            
            confirmed_df = df[df['status'] == 'Confirmed'].sort_values(['country', 'league_name'])
            for _, league in confirmed_df.iterrows():
                f.write(f"   ✅ {league['league_name']:<30} (ID: {league['season_id']:<6}) - {league['country']}\n")
            
            f.write(f"\n📋 ESTIMATED 2025 SEASON IDs (Need Verification):\n")
            f.write("=" * 55 + "\n\n")
            
            estimated_df = df[df['status'] == 'Estimated'].sort_values(['country', 'league_name'])
            
            # Group estimated by country
            for country in estimated_df['country'].unique():
                country_estimated = estimated_df[estimated_df['country'] == country]
                f.write(f"🌍 {country}:\n")
                for _, league in country_estimated.iterrows():
                    f.write(f"   📋 {league['league_name']:<30} (ID: {league['season_id']:<6})\n")
                f.write("\n")
            
            f.write("📈 REGIONAL BREAKDOWN:\n")
            f.write("=" * 22 + "\n\n")
            
            regional_summary = df.groupby('country').agg({
                'estimated_matches': 'sum',
                'league_name': 'count',
                'status': lambda x: (x == 'Confirmed').sum()
            }).rename(columns={
                'league_name': 'total_leagues',
                'status': 'confirmed_ids'
            }).sort_values('estimated_matches', ascending=False)
            
            for country, stats in regional_summary.iterrows():
                f.write(f"   {country:<15}: {int(stats['total_leagues']):2} leagues, {int(stats['estimated_matches']):4} matches, {int(stats['confirmed_ids']):2} confirmed\n")
            
            f.write(f"\n⚠️ LEGEND:\n")
            f.write("✅ = Season ID confirmed from official sources\n")
            f.write("📋 = Season ID estimated/calculated (needs verification)\n")
            f.write("\n📝 NOTES:\n")
            f.write("• All leagues support comprehensive betting markets\n")
            f.write("• Estimated matches based on typical league formats\n")
            f.write("• Season years vary by region (2025 vs 2025-26)\n")
            f.write("• Continental competitions depend on qualification stages\n")
            f.write("• Cup competitions may have variable match counts\n")
        
        print(f"📋 Report saved: all_2025_leagues_with_ids_{timestamp}.txt")
        
        # Create summary CSV
        csv_filename = f"/Users/richardgibbons/soccer betting python/soccer/output reports/2025_leagues_master_list_{timestamp}.csv"
        
        summary_data = []
        for _, league in df.iterrows():
            summary_data.append({
                'league_name': league['league_name'],
                'country': league['country'],
                'tier': league['tier'],
                'season_id': league['season_id'],
                'season_year': league['season_year'],
                'status': league['status'],
                'start_month': league['typical_start'],
                'end_month': league['typical_end'],
                'estimated_matches': league['estimated_matches'],
                'betting_markets': league['betting_markets_available']
            })
        
        # Save CSV
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = [
                'league_name', 'country', 'tier', 'season_id', 'season_year', 
                'status', 'start_month', 'end_month', 'estimated_matches', 'betting_markets'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in summary_data:
                writer.writerow(row)
        
        print(f"💾 CSV saved: 2025_leagues_master_list_{timestamp}.csv")
        
        # Print key statistics
        print(f"\n📊 KEY STATISTICS:")
        print(f"   📋 Total Leagues: {len(df)}")
        print(f"   ✅ Confirmed Season IDs: {confirmed_leagues}")
        print(f"   📋 Estimated Season IDs: {estimated_leagues}")
        print(f"   ⚽ Total Estimated Matches: {total_matches:,}")
        print(f"   🌍 Countries: {df['country'].nunique()}")
        
        print(f"\n🏆 TOP 5 COUNTRIES BY LEAGUE COUNT:")
        top_countries = regions.head(5)
        for country, count in top_countries.items():
            confirmed_count = len(df[(df['country'] == country) & (df['status'] == 'Confirmed')])
            print(f"   {country}: {count} leagues ({confirmed_count} confirmed)")
        
        return df
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find 2025 leagues file: {leagues_2025_file}")
        return None
    except Exception as e:
        print(f"❌ Error processing 2025 leagues data: {e}")
        return None


def main():
    """Generate 2025 leagues report"""
    
    print("📋 Starting 2025 Leagues & IDs Report Generation...")
    
    df = generate_simple_2025_report()
    
    if df is not None:
        print(f"\n✅ 2025 Leagues & IDs Report Generated Successfully!")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"📁 Files created:")
        print(f"   • all_2025_leagues_with_ids_{timestamp}.txt")
        print(f"   • 2025_leagues_master_list_{timestamp}.csv")
    else:
        print("❌ Failed to generate report")


if __name__ == "__main__":
    main()