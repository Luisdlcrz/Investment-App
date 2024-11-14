import streamlit as st
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objs as go
import pandas as pd
import appdirs as ad
ad.user_cache_dir = lambda *args: "/tmp"
import yfinance as yf
import riskfolio as rp
import numpy as np
from scipy.optimize import minimize

# Set page config
st.set_page_config(page_icon=":chart_with_upwards_trend:", page_title="InvTech", layout="centered")

# Initialize session state for navigation if not already set
if "page" not in st.session_state:
    st.session_state.page = "home"

# Function to navigate to the quiz page
def go_to_quiz():
    st.session_state.page = "quiz"

# Function to navigate to page 2
def go_to_page_2():
    st.session_state.page = "page_2"

# Function to navigate to final page
def go_to_final_page():
    st.session_state.page = "final_page"


# Home page content
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center;'>Welcome to InvTech Portfolio Management!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Click below to start assessing your portfolio.</p>", unsafe_allow_html=True)

    # Centered "Start Quiz" button using Streamlit's st.button
    st.markdown(
        """
        <style>
            .center-button {
                display: flex;
                justify-content: center;
            }
            .big-button {
                font-size: 20px;
                width: 200px;
                height: 60px;
                text-align: center;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
            }
            .big-button:hover {
                background-color: #45a049;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Button for starting the quiz, centered
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Start Quiz", on_click=go_to_quiz, key="start_quiz"):
            pass



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
### PAGE 1: RISK TOLERANCE QUIZ ###
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #


# Quiz page content
if st.session_state.page == "quiz":
    st.header("Investment Risk Tolerance Quiz")

    # Quiz questions, options, and scores
    questions = {
        "1. In general, how would your best friend describe you as a risk taker?": {
            "options": ["A real gambler", "Willing to take risks after completing adequate research",
                        "Cautious", "A real risk avoider"],
            "scores": [4, 3, 2, 1]
        },
        "2. You are on a TV game show and can choose one of the following. Which would you take?": {
            "options": ["$1,000 in cash", "A 50% chance at winning $5,000",
                        "A 25% chance at winning $10,000", "A 5% chance at winning $100,000"],
            "scores": [1, 2, 3, 4]
        },
        "3. You have just finished saving for a “once-in-a-lifetime” vacation. Three weeks before you plan to leave, you lose your job. You would:": {
            "options": ["Cancel the vacation",
                        "Take a much more modest vacation",
                        "Go as scheduled, reasoning that you need the time to prepare for a job search",
                        "Extend your vacation, because this might be your last chance to go first-class"],
            "scores": [1, 2, 3, 4]
        },
        "4. If you unexpectedly received $20,000 to invest, what would you do?": {
            "options": ["Deposit it in a bank account, money market account, or an insured CD",
                        "Invest it in safe high quality bonds or bond mutual funds",
                        "Invest it in stocks or stock mutual funds"],
            "scores": [1, 2, 3]
        },
        "5. In terms of experience, how comfortable are you investing in stocks or stock mutual funds?": {
            "options": ["Not at all comfortable",
                        "Somewhat comfortable",
                        "Very comfortable"],
            "scores": [1, 2, 3]
        },
        "6. When you think of the word “risk” which of the following words comes to mind first? ": {
            "options": ["Loss",
                        "Uncertainty",
                        "Opportunity",
                        "Thrill"],
            "scores": [1, 2, 3, 4]
        },
        "7. Some experts are predicting prices of assets such as gold, jewels, collectibles, and real estate (hard assets) to increase in value; bond prices may fall, however, experts tend to agree that government bonds are relatively safe. Most of your investment assets are now in high-interest government bonds. What would you do?": {
            "options": ["Hold the bonds",
                        "Sell the bonds, put half the proceeds into money market accounts, and the other half into hard assets",
                        "Sell the bonds and put the total proceeds into hard assets",
                        "Sell the bonds, put all the money into hard assets, and borrow additional money to buy more"],
            "scores": [1, 2, 3, 4]
        },
        "8. Given the best and worst case returns of the four investment choices below, which would you prefer?": {
            "options": ["\$200 gain best case, \$0 gain/loss worst case",
                        "\$800 gain best case, \$200 loss worst case",
                        "\$2,600 gain best case, \$800 loss worst case",
                        "\$4,800 gain best case, \$2,400 loss worst case"],
            "scores": [1, 2, 3, 4]
        },
        "9. In addition to whatever you own, you have been given $1,000. You are now asked to choose between:": {
            "options": ["A sure gain of $500",
                        "A 50% chance to gain $1,000 and a 50% chance to gain nothing"],
            "scores": [1, 3]
        },
        "10. In addition to whatever you own, you have been given $2,000. You are now asked to choose between:": {
            "options": ["A sure loss of $500",
                        "A 50% chance to lose $1,000 and a 50% chance to lose nothing"],
            "scores": [1, 3]
        },
        "11. Suppose a relative left you an inheritance of $100,000, stipulating in the will that you invest ALL the money in ONE of the following choices. Which one would you select?": {
            "options": ["A savings account or money market mutual fund",
                        "A mutual fund that owns stocks and bonds",
                        "A portfolio of 15 common stocks",
                        "Commodities like gold, silver, and oil"],
            "scores": [1, 2, 3, 4]
        },
        "12. If you had to invest $20,000, which of the following investment choices would you find most appealing?": {
            "options": ["60% in low-risk investments, 30% in medium-risk investments, 10% in high-risk investments",
                        "30% in low-risk investments, 40% in medium-risk investments, 30% in high-risk investments",
                        "10% in low-risk investments, 40% in medium-risk investments, 50% in high-risk investments"],
            "scores": [1, 2, 3]
        },
        "13. Your trusted friend and neighbor, an experienced geologist, is putting together a group of investors to fund an exploratory gold mining venture. The venture could pay back 50 to 100 times the investment if successful. If the mine is a bust, the entire investment is worthless. Your friend estimates the chance of success is only 20%. If you had the money, how much would you invest? ": {
            "options": ["Nothing",
                        "One month’s salary",
                        "Three month’s salary",
                        "Six month’s salary"],
            "scores": [1, 2, 3, 4]
        }
    }

    # Store user's responses
    user_answers = {}
    for i, (question, data) in enumerate (questions.items()):
        st.subheader(question)
        key = f"question_{i}" # Create a unique key for each question
        if key not in st.session_state:
            st.session_state[key] = None # Initialize with None
        user_answers[question] = st.radio("Select your answer:", data["options"], key=key, index=None)

    # Display questions and get user input
    for question, data in questions.items():
        st.subheader(question)
        user_answers[question] = st.radio("Select your answer:", data["options"], key=question)


    # "Submit" button with st.button()
    submit_button = st.markdown(
        """
        <style>
            div.stButton > button {
                display: block;
                margin: 0 auto;
                font-size: 20px;
                width: 150px;
                height: 50px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
            }
            div.stButton > button:hover {
                background-color: #45a049;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Check answers and display score when "Submit" button is clicked
    if st.button("Submit"):
        score = sum(data["scores"][data["options"].index(user_answers[question])] for question, data in questions.items())

        # Display a centered thank-you message and score
        st.markdown(
            f"""
            <div style="text-align: center; font-size: 20px;">
                Thank you for taking the quiz! <br>
                Your score is: <strong>{score}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Define risk tolerance categories
        risk_tolerance_categories = {
            (0, 18): "Low risk tolerance (i.e., conservative investor)",
            (19, 22): "Below-average risk tolerance",
            (23, 28): "Average/moderate risk tolerance",
            (29, 32): "Above-average risk tolerance",
            (33, float('inf')): "High risk tolerance (i.e., aggressive investor)"
        }


        # Determine the risk tolerance category
        risk_tolerance = None
        for score_range, tolerance in risk_tolerance_categories.items():
            if score_range[0] <= score <= score_range[1]:
                risk_tolerance = tolerance
                break

        # Center the risk tolerance message using HTML
        if risk_tolerance:
            st.markdown(
                f"""
                <div style="text-align: center; font-size: 20px;">
                    Your risk tolerance level is: <strong>{risk_tolerance}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="text-align: center; font-size: 20px; color: red;">
                    Risk tolerance level not found. Please complete the quiz.
                </div>
                """,
                unsafe_allow_html=True
            )


        # Store risk tolerance in session state
        st.session_state.risk_tolerance_level = risk_tolerance  # Save the result in session state

        # Display the risk tolerance
        st.markdown(f"Your risk tolerance level: **{risk_tolerance}**")

        # Add a button to go to the next page
        if st.button("Next", on_click=go_to_page_2, key="page_2"):
            pass

# %%%%%%%%%%%%%%%%%%%%%%%%%%%% #
### PAGE 2: COMPARING STOCKS & GOLDEN/DEATH CROSS ###
# %%%%%%%%%%%%%%%%%%%%%%%%%%%% #

if st.session_state.page == "page_2":
    st.title("Financial Comparison of Two Companies")

    # User inputs for company symbols
    st.subheader("Compare Two Companies")
    company1 = st.text_input("Please enter first stock ticker (e.g., TSLA):", "TSLA")
    company2 = st.text_input("Please enter second stock ticker (e.g., TSLA):", "TSLA")

    if company1 and company2:
        # Fetch and display financial metrics for both companies
        def get_financial_metrics(symbol):
            stock = yf.Ticker(symbol)
            balance_sheet = stock.balance_sheet
            income_statement = stock.financials

            # Debt-to-Equity Ratio
            debt_to_equity = stock.info.get('debtToEquity', None)

            # Revenue Growth
            revenue_growth = ((income_statement.loc['Total Revenue'].iloc[0] - income_statement.loc['Total Revenue'].iloc[1]) /
                              income_statement.loc['Total Revenue'].iloc[1]) * 100

            # Return on Equity (ROE)
            roe = stock.info.get('returnOnEquity', None)

            # Dividend Payout Ratio
            dividend_payout_ratio = stock.info.get("payoutRatio", None)

            # Dividend Yield
            dividends_per_share = stock.info.get('dividendRate', 0)  # Get dividends per share
            dividend_yield = (dividends_per_share / stock.info['previousClose']) * 100

            # Beta
            beta = stock.info.get('beta', None)

            return {"Debt-to-Equity": debt_to_equity, "Revenue Growth": revenue_growth, "ROE": roe, "Dividend-Payout Ratio": dividend_payout_ratio, "Dividend Yield": dividend_yield,  "Beta": beta}

        def evaluate_metrics(symbol):
            stock = yf.Ticker(symbol)
            balance_sheet = stock.balance_sheet
            income_statement = stock.financials

            # Debt-to-Equity Ratio
            debt_to_equity = stock.info.get('debtToEquity', None)

            # Revenue Growth
            revenue_growth = ((income_statement.loc['Total Revenue'].iloc[0] - income_statement.loc['Total Revenue'].iloc[1]) /
                                  income_statement.loc['Total Revenue'].iloc[1]) * 100

            # Return on Equity (ROE)
            roe = stock.info.get('returnOnEquity', None)

            # Dividend Payout Ratio
            dividend_payout_ratio = stock.info.get("payoutRatio", None)

            # Dividend Yield
            dividends_per_share = stock.info.get('dividendRate', 0)  # Get dividends per share
            dividend_yield = (dividends_per_share / stock.info['previousClose']) * 100

            # Beta
            beta = stock.info.get('beta', None)

            # Evaluate Debt-to-Equity Ratio
            if debt_to_equity is not None:
              try:
                debt_to_equity = float(debt_to_equity)
                if debt_to_equity < 1:
                    debt_to_equity_rating = "Low (Good)"
                elif debt_to_equity < 2:
                    debt_to_equity_rating = "Moderate"
                else:
                    debt_to_equity_rating = "High (Risky)"
              except (TypeError, ValueError):
                debt_to_equity_rating = "N/A"
            else:
                debt_to_equity_rating = "N/A"

            # Evaluate Revenue Growth
            if revenue_growth is not None: 
              try: 
                revenue_growth = float(revenue_growth)
                if revenue_growth >= 5:
                    revenue_growth_rating = "Consistent Growth"
                elif revenue_growth > 0:
                    revenue_growth_rating = "Positive but Low Growth"
                else:
                    revenue_growth_rating = "Declining Revenue"
              except (TypeError, ValueError):
                revenue_growth_rating = "N/A"
            else:
                revenue_growth_rating = "N/A"      

            # Evaluate ROE
            if roe is not None:
              try:
                roe = float(roe)
                if roe >= 20:
                    roe_rating = "Very High (Excellent)"
                elif roe >= 15:
                    roe_rating = "High (Good)"
                else:
                    roe_rating = "Low"
              except (TypeError, ValueError):
                roe_rating = "N/A"
            else:
                roe_rating = "N/A"

            # Evaluate Payout Ratio
            if dividend_payout_ratio is not None:
              try:
                dividend_payout_ratio = float(dividend_payout_ratio)
                if dividend_payout_ratio < 60:
                    dividend_payout_ratio_rating = "Healthy."
                elif dividend_payout_ratio <= 75:
                    dividend_payout_ratio_rating = "Moderate."
                else:
                    dividend_payout_ratio = "Risky."
              except (TypeError, ValueError):
                dividend_payout_ratio_rating = "N/A"
            else:
                dividend_payout_ratio_rating = "N/A"

            # Dividend History (Checking last few years)
            dividends = stock.dividends
            if len(dividends) > 12:
                dividend_payout = "has a history of paying dividends."
            else:
                dividend_payout = "none"

            # Evaluate Dividend Yield
            industry_avg_yield = 2.5 # Industry average yield for comparison!!!
            if dividend_yield is not None:
              if dividend_yield < industry_avg_yield:
                  yield_rating = "Low"
              elif dividend_yield <= industry_avg_yield * 1.5:
                  yield_rating = "Healthy"
              else:
                  yield_rating = "High (Potential Risk)"
            else:
                yield_rating = "N/A"

            # Evaluate Beta
            if beta is not None:
              try:
                beta = float(beta)
                if beta < 0:
                    beta_rating = "This stock has a negative beta, meaning it tends to move inversely to the market. It may provide a hedge against market downturns."
                elif beta < 1:
                    beta_rating = "This stock has a low beta, meaning it is less volatile than the market. It may be suitable for conservative investors looking for stability."
                elif beta <= 1.5:
                    beta_rating = "This stock has a moderate beta, meaning it tends to move in line with the market. It has average market risk."
                else:
                    beta_rating = "This stock has a high beta, meaning it is more volatile than the market. It may appeal to aggressive investors willing to take on more risk for potentially higher returns."
              except (TypeError, ValueError):
                beta_rating = "N/A"
            else:
              beta_rating = "N/A"

            return {
                "Debt-to-Equity": debt_to_equity_rating,
                "Revenue Growth": revenue_growth_rating,
                "ROE": roe_rating,
                "Dividend History": dividend_payout,
                "Dividend-Payout Ratio": dividend_payout_ratio_rating,
                "Dividend Yield": yield_rating,
                "Beta": beta_rating
                }

        # Display metrics for each company
        metrics1 = get_financial_metrics(company1)
        metrics12= evaluate_metrics(company1)
        metrics2 = get_financial_metrics(company2)
        metrics22= evaluate_metrics(company2)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"Metrics for {company1}")
            for metric, value in metrics1.items():
                if value is not None: 
                  st.write(f"**{metric}:** {value}")
                else:
                  st.write(f"**{metric}:** N/A")

        with col1:
            st.subheader(f"Rating for {company1}")
            for metric, value in metrics12.items():
                if value is not None: 
                  st.write(f"**{metric}:** {value}")
                else:
                  st.write(f"**{metric}:** N/A")

        with col2:
            st.subheader(f"Metrics for {company2}")
            for metric, value in metrics2.items():
                if value is not None: 
                  st.write(f"**{metric}:** {value}")
                else:
                  st.write(f"**{metric}:** N/A")


        with col2:
            st.subheader(f"Rating for {company2}")
            for metric, value in metrics22.items():
                if value is not None: 
                  st.write(f"**{metric}:** {value}")
                else:
                  st.write(f"**{metric}:** N/A")

        # Plot Golden/Death Cross
        def plot_golden_death_cross(symbol):
            data = yf.download(symbol, start="2022-01-01")['Adj Close']
            short_ma = data.rolling(window=50).mean()
            long_ma = data.rolling(window=200).mean()

            plt.figure(figsize=(12, 6))
            plt.plot(data, label="Price")
            plt.plot(short_ma, label="50-day MA", linestyle="--")
            plt.plot(long_ma, label="200-day MA", linestyle="--")
            plt.legend()
            plt.title(f"Golden/Death Cross for {symbol}")
            st.pyplot(plt)

        st.subheader("**Golden/Death Cross for Selected Stocks**")
        st.subheader("The golden cross & death cross are two technical indicators that help signal potential trends on stock prices, based on the movement of two moving averages. Golden Cross: This occurs when a short-term moving average (50-day moving average) crosses above a long-term moving average (200-day) moving average). The golden cross generally is viewed as a bullish signal, suggesting that the stocks momentum is shifting upward and that a potential uptrend may be beginning. Time to buy! Death Cross: This is the opposite scenario, where the short-term moving average crosses below the long-term moving average. The death cross is considered a bearish signal, indicating that downward momentum may continue & that the stock could be entering a downtrend. Sell before it is too late!")
        
        plot_golden_death_cross(company1)
        plot_golden_death_cross(company2)

        try:
            # Compare stock price movements
            data1 = yf.download(company1, start="2023-01-01")['Adj Close']
            data2 = yf.download(company2, start="2023-01-01")['Adj Close']

            plt.figure(figsize=(12, 6))
            plt.plot(data1, label=company1)
            plt.plot(data2, label=company2)
            plt.xlabel("Date")
            plt.ylabel("Adjusted Close Price")
            plt.title(f"Price Comparison: {company1} vs {company2}")
            plt.legend()
            st.pyplot(plt)
        except Exception as e:
            st.error(f"Error fetching data: {e}")
    else:
        st.error("Please enter both company symbols for comparison.")

    if st.button("Next", on_click=go_to_final_page, key="final_page"):
        pass


# %%%%%%%%%%%%%%%%%%%%%%%%%%%% #
### FINAL PAGE: PORTFOLIO BUILDER ###
# %%%%%%%%%%%%%%%%%%%%%%%%%%%% #

# Portfolio Optimization function (Mean-Variance Optimization)
def optimize_portfolio(returns, risk_free_rate=0.0):
    # Objective function: Minimize portfolio variance (risk)
    def objective(weights):
        return np.dot(weights.T, np.dot(returns.cov(), weights))

    # Constraints: Weights must sum to 1 (fully invested)
    def constraint(weights):
        return np.sum(weights) - 1

    # Bounds for each weight: between 0 and 1
    bounds = [(0, 1) for _ in range(len(returns.columns))]

    # Initial guess (equal distribution)
    initial_guess = [1. / len(returns.columns)] * len(returns.columns)

    # Solve the optimization problem
    result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints={'type': 'eq', 'fun': constraint})

    return result.x  # Optimal weights


# Portfolio Builder page content
if st.session_state.page == "final_page":
    st.title("Portfolio Builder")

    # Investment amount input
    investment_amount = st.number_input("Enter total investment amount:", min_value=0.0, step=1000.0)

    # Risk Tolerance-Based Stock Selection
    if "risk_tolerance_level" in st.session_state:
        risk_tolerance = st.session_state.risk_tolerance_level
        if risk_tolerance == "Low risk tolerance (i.e., conservative investor)":
            stock_options = ["VTI", "BND", "AGG", "XLP", "VZ"]
            st.write("Based on your low risk tolerance, we recommend considering the following stocks:")
        elif risk_tolerance == "Below-average risk tolerance":
            stock_options = ["VUG", "VO", "VEA", "KO", "PG"]
            st.write("Based on your below-average risk tolerance, we recommend considering the following stocks:")
        elif risk_tolerance == "Average/moderate risk tolerance":
            stock_options = ["QQQ", "SPY", "IVV", "MSFT", "JNJ"]
            st.write("Based on your average risk tolerance, we recommend considering the following stocks:")
        elif risk_tolerance == "Above-average risk tolerance":
            stock_options = ["ARKK", "TQQQ", "XLK", "TSLA", "NVDA"]
            st.write("Based on your above-average risk tolerance, we recommend considering the following stocks:")
        elif risk_tolerance == "High risk tolerance (i.e., aggressive investor)":
            stock_options = ["FDN", "SPYD", "XLY", "AMZN", "BABA"]
            st.write("Based on your high risk tolerance, we recommend considering the following stocks:")
        else:
            st.warning("Please complete the Risk Tolerance Quiz first to get stock suggestions.")

        # Input for stock selection (multiselect)
        selected_stocks = st.multiselect("Select Stocks:", stock_options)

        # Input for investment amount for each selected stock
        stock_allocations = {}
        for stock in selected_stocks:
            allocation = st.number_input(f"Investment amount for {stock}:", min_value=0.0, max_value=investment_amount, step=100.0)
            stock_allocations[stock] = allocation

        # Check if user has selected stocks and allocated investments
        if selected_stocks and all(allocation > 0 for allocation in stock_allocations.values()):
            try:
                # Fetch historical adjusted close price data for selected stocks
                stock_data = yf.download(selected_stocks, start="2023-01-01")['Adj Close']

                # Calculate daily returns (percentage change)
                returns = stock_data.pct_change().dropna()

                # Optimize portfolio weights (minimize risk)
                optimal_weights = optimize_portfolio(returns)

                # Calculate portfolio composition (weight allocation)
                portfolio_composition = {selected_stocks[i]: optimal_weights[i] for i in range(len(selected_stocks))}

                # Display portfolio composition
                st.write("**Optimal Portfolio Weights (Minimized Risk):**")
                for stock, weight in portfolio_composition.items():
                    st.write(f"{stock}: {weight * 100:.2f}%")

                # Display Pie Chart of Portfolio Composition
                fig, ax = plt.subplots()
                ax.pie(optimal_weights, labels=selected_stocks, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                st.pyplot(fig)

                # Display total value of portfolio based on the user's investment amount
                portfolio_value = sum(stock_allocations[stock] * portfolio_composition[stock] for stock in selected_stocks)
                st.write(f"**Total Portfolio Value**: ${portfolio_value:.2f}")

            except Exception as e:
                st.error(f"Error building portfolio: {e}")

        else:
            st.warning("Please ensure you have selected stocks and allocated investments.")



