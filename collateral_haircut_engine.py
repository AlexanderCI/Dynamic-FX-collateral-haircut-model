# assignment / portfolio project for dynamic liquidity risk tracking
# applying basic actuarial tail-risk metrics (VaR/ES) to treasury collateral management

import numpy as np
import pandas as pd

def run_haircut_engine():
    # step 1: load up our market data sheet
    try:
        market_data = pd.read_csv('fx_market_history.csv')
    except:
        print("Error: check your file path, fx_market_history.csv is missing!")
        return

    print("=====================================================================")
    print("     STARTING DYNAMIC FX COLLATERAL HAIRCUT SIMULATION ENGINE        ")
    print("=====================================================================\n")

    # step 2: calculate log returns for all foreign currencies relative to CAD
    currencies = ['USD_CAD', 'EUR_CAD', 'GBP_CAD', 'AUD_CAD']
    returns_df = pd.DataFrame()
    
    for ccypair in currencies:
        # using standard log returns like we do in financial modeling classes
        returns_df[ccypair] = np.log(market_data[ccypair] / market_data[ccypair].shift(1))
    
    # drop the first row since shifting leaves a NaN
    returns_df = returns_df.dropna()

    # step 3: calculate dynamic haircuts using Expected Shortfall (99% confidence)
    # ES is way better than VaR because it actually tells you what happens inside the disaster tail
    haircut_dict = {}
    confidence_level = 0.99

    print("--- Calculating Tail Risk & Historical Haircuts (10-Day Window) ---")
    for ccypair in currencies:
        ccy_returns = returns_df[ccypair].values
        
        # find the lower percentile threshold (Value at Risk)
        var_threshold = np.percentile(ccy_returns, (1 - confidence_level) * 100)
        
        # Expected Shortfall is the average of all returns that breached the VaR line
        tail_losses = ccy_returns[ccy_returns <= var_threshold]
        
        if len(tail_losses) == 0:
            # safety net if data sample is tiny
            expected_shortfall = var_threshold
        else:
            expected_shortfall = np.mean(tail_losses)
            
        # we scale the daily tail risk to a 10-day liquidity horizon using square-root-of-time rule
        scaled_risk = abs(expected_shortfall) * np.sqrt(10)
        
        # add a flat 2% buffer just to cover operational execution delays during a market freeze
        final_dynamic_haircut = scaled_risk + 0.02
        
        # save the haircut metric to use on our portfolio
        haircut_dict[ccypair] = final_dynamic_haircut
        print(f"Currency: {ccypair[:3]} | 99% ES (Daily): {abs(expected_shortfall):.4f} | Dynamic 10D Haircut: {final_dynamic_haircut*100:.2f}%")
    print("---------------------------------------------------------------------\n")

    # step 4: load up our current portfolio of pledged collateral from partner states
    # assuming we hold a bunch of nominal sovereign deposits that need validation
    mock_collateral_pool = {
        'USD_CAD': 450000000.0, # $450M USD value pledged
        'EUR_CAD': 350000000.0, # $350M EUR value pledged
        'GBP_CAD': 250000000.0, # $250M GBP value pledged
        'AUD_CAD': 150000000.0  # $150M AUD value pledged
    }
    
    # baseline cash cushion we need to guarantee our short-term obligations
    required_liquidity_floor = 1000000000.0 # $1B CAD framework target

    print("--- Applying Dynamic Haircuts to Active Treasury Collateral Pool ---")
    total_nominal_value = 0.0
    total_post_haircut_value = 0.0
    
    print(f"{'Asset Pool':<12} | {'Nominal Value (CAD)':<20} | {'Haircut applied':<15} | {'Liquidity Value':<18}")
    print("-" * 75)
    
    for ccy, nominal in mock_collateral_pool.items():
        haircut_pct = haircut_dict[ccy]
        discounted_value = nominal * (1 - haircut_pct)
        
        total_nominal_value += nominal
        total_post_haircut_value += discounted_value
        
        print(f"{ccy[:3] + '_Pool':<12} | ${nominal:18,.2f} | {haircut_pct*100:13.2f}% | ${discounted_value:16,.2f}")
        
    print("-" * 75)
    print(f"Total Portfolio Face Value:         ${total_nominal_value:,.2f}")
    print(f"Total Realizable Liquidity Cushion:  ${total_post_haircut_value:,.2f}")
    print(f"Target Treasury Liquidity Floor:     ${required_liquidity_floor:,.2f}")
    print("---------------------------------------------------------------------\n")

    # step 5: structural balance sheet evaluation
    net_buffer_margin = total_post_haircut_value - required_liquidity_floor
    
    print("--- Executive Risk Assessment ---")
    if net_buffer_margin < 0:
        print(f"RISK SIGNAL: Liquidity deficit detected! Deficit size: ${abs(net_buffer_margin):,.2f}")
        print("Action Required: Call for additional member margin injections or hedge the FX corridor exposure immediately.")
    else:
        print(f"STATUS REPORT: Collateral buffers are solid. Surplus margin: ${net_buffer_margin:,.2f}")
        print("No immediate open-market asset liquidations required.")
    print("=====================================================================\n")

if __name__ == "__main__":
    run_haircut_engine()
