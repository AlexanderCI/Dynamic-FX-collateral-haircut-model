# Dynamic FX Collateral Haircut Model (Liquidity Optimization)

Hey everyone! This is a project I put together combining some of the financial econ and stochastic risk concepts from my actuarial coursework at UofT. 

The goal here is to solve a really annoying problem that multi-currency development banks face: **Collateral Liquidity Volatility**. When an international institution takes sovereign bonds or foreign currencies as collateral from different member countries, it has to apply a "haircut" (basically a discount) to protect itself. If a crisis hits and a foreign currency tanks, a fixed haircut won't save you from a major liquidity outflow.

This script builds a dynamic framework to calculate Value at Risk (VaR) and Expected Shortfall (ES) on historical FX returns. It simulates how much our collateral buffer could evaporate during a 10-day market panic/stress scenario.

### High level overview of what this does:
1. Loads up a mock timeseries of daily FX rates for a few different currency blocks (think major alliance nations).
2. It computes rolling historical volatility and daily returns.
3. Calculates a dynamic liquidity haircut based on a 99% Expected Shortfall metric (tail risk).
4. Finally, it runs a stress test on a mock portfolio of pledged collateral to see if the bank faces a liquidity deficit under extreme conditions.

Feel free to look through the code or mess with the parameters! Always open to feedback on my modeling assumptions.
