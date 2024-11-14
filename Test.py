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
            # Calculate the score
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

            # Determine risk tolerance level and display it with only risk tolerance in bold
            for score_range, risk_tolerance in risk_tolerance_categories.items():
                if score_range[0] <= score <= score_range[1]:
                    st.session_state.risk_tolerance_level = risk_tolerance
                    st.markdown(
                        f"""
                        <div style="text-align: center; font-size: 22px;">
                            Your risk tolerance level: <strong>{risk_tolerance}</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
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
            debt_to_equity = balance_sheet.loc['Total Liabilities Net Minority Interest'].iloc[0] / balance_sheet.loc['Stockholders Equity'].iloc[0]

            # Revenue Growth
            revenue_growth = ((income_statement.loc['Total Revenue'].iloc[0] - income_statement.loc['Total Revenue'].iloc[1]) /
                              income_statement.loc['Total Revenue'].iloc[1]) * 100

            # Return on Equity (ROE)
            roe = (income_statement.loc['Net Income'].iloc[0] / balance_sheet.loc['Stockholders Equity'].iloc[0]) * 100

            return {"Debt-to-Equity": debt_to_equity, "Revenue Growth": revenue_growth, "ROE": roe}

        # Display metrics for each company
        metrics1 = get_financial_metrics(company1)
        metrics2 = get_financial_metrics(company2)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"Metrics for {company1}")
            for metric, value in metrics1.items():
                st.write(f"**{metric}:** {value:.2f}")

        with col2:
            st.subheader(f"Metrics for {company2}")
            for metric, value in metrics2.items():
                st.write(f"**{metric}:** {value:.2f}")

        # Plot Golden/Death Cross
        def plot_golden_death_cross(symbol):
            data = yf.download(symbol, start="2022-01-01")['Adj Close']
            short_ma = data.rolling(window=50).mean()
            long_ma = data.rolling(window=200).mean()

            plt.figure(figsize=(12, 6))
            plt.plot(data, label="Price")
            plt.plot(short_ma, label="50-day MA (Golden Cross)", linestyle="--")
            plt.plot(long_ma, label="200-day MA (Death Cross)", linestyle="--")
            plt.legend()
            plt.title(f"Golden/Death Cross for {symbol}")
            st.pyplot(plt)

        st.write("**Golden/Death Cross for Selected Stocks**")
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
# %%%%%%%%%%%%%%%%%%%%%%%%%%%% #
### FINAL PAGE: PORTFOLIO BUILDER ###
# %%%%%%%%%%%%%%%%%%%%%%%%%%%% #
if st.session_state.page == "final_page":
    st.title("Portfolio Builder")

    # Investment amount input
    #investment_amount = st.number_input("Enter total investment amount:", min_value=0.0, step=1000.0)

    # Ensure the risk tolerance level from the quiz is stored in the session state
    if "risk_tolerance_level" not in st.session_state:
        st.warning("Please complete the Risk Tolerance Quiz first to get stock suggestions.")
    else:
        risk_tolerance = st.session_state.risk_tolerance_level

        # Stock recommendations based on risk tolerance
        if risk_tolerance == "Low risk tolerance (i.e., conservative investor)":
            stock_options = ["VTI", "BND", "AGG", "XLP", "VZ"]  # Examples of low-risk stocks (broad market, bonds)
            st.write("Based on your low risk tolerance, we recommend considering the following stocks:")
        elif risk_tolerance == "Below-average risk tolerance":
            stock_options = ["VUG", "VO", "VEA", "KO", "PG"]  # Examples of below-average risk stocks (growth, value)
            st.write("Based on your below-average risk tolerance, we recommend considering the following stocks:")
        elif risk_tolerance == "Average/moderate risk tolerance":
            stock_options = ["QQQ", "SPY", "IVV", "MSFT", "JNJ"]  # Examples of moderate risk stocks (tech, S&P 500)
            st.write("Based on your average risk tolerance, we recommend considering the following stocks:")
        elif risk_tolerance == "Above-average risk tolerance":
            stock_options = ["ARKK", "TQQQ", "XLK", "TSLA", "NVDA"]  # Examples of above-average risk stocks (innovation, tech)
            st.write("Based on your above-average risk tolerance, we recommend considering the following stocks:")
        elif risk_tolerance == "High risk tolerance (i.e., aggressive investor)":
            stock_options = ["FDN", "SPYD", "XLY", "AMZN", "BABA"]  # Examples of high-risk stocks (high-dividend, retail)
            st.write("Based on your high risk tolerance, we recommend considering the following stocks:")

        # Input for stock selection (multiselect)
        selected_stocks = st.multiselect("Select Stocks:", stock_options)

        # Proceed only if stocks are selected
        if selected_stocks:
            # Fetch historical data for selected stocks
            try:
                stock_data = yf.download(selected_stocks, start="2023-01-01")['Adj Close']
                rets = stock_data.pct_change().dropna()  # Calculate daily returns
                
                # Calculate optimal portfolio using riskfolio
                port = rp.Portfolio(returns=rets)
                port.assets_stats(method_mu='hist', method_cov='hist')  # Historical mean and covariance
             
                # Weights in case of minimizing risk
                min_risk_weights = port.optimization(model='Classic', rm='MV', obj='MinRisk', rf=0, hist=True)
                st.write("**Optimal Portfolio Weights (Minimizing Risk)**")
                st.write(min_risk_weights.T)

                # Display portfolio composition for minimizing risk
                fig, ax = plt.subplots(figsize=(10, 8))
                rp.plot_pie(min_risk_weights, title="Optimal Portfolio Composition (Minimizing Risk)", ax=ax)
                st.pyplot(fig)

                # Weights in case of maximizing returns
                #max_return_weights = port.optimization(model='Classic', rm='MV', obj='MaxRet', rf=0.5, hist=True)
                #st.write("**Optimal Portfolio Weights (Maximizing Returns)**")
                #st.write(max_return_weights.T)

                # Display portfolio composition for maximizing returns
                #fig, ax = plt.subplots(figsize=(10, 8))
                #rp.plot_pie(max_return_weights, title="Optimal Portfolio Composition (Maximizing Returns)", ax=ax)
                #st.pyplot(fig)

            except Exception as e:
                st.error(f"Error building portfolio: {e}")
    #else:
        #st.warning("Please complete the Risk Tolerance Quiz first to get stock suggestions.")
