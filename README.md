# Indian Gold Rate Tracker

![2nd SS](https://github.com/user-attachments/assets/cd672ca0-d68a-4e02-9243-6bdf4bb47c0d)

![1st SS](https://github.com/user-attachments/assets/c01f590b-1a24-4fac-8595-4ad4214d516b)

![3rd SS](https://github.com/user-attachments/assets/1e91c84c-a6e3-43c4-aefe-20a06b24f4ce)


A Streamlit application that tracks and visualizes gold rates in India across different purities (24K, 22K, 18K, and 14K).

## Features

- Real-time gold rate tracking
- Multiple purity rate calculations (24K, 22K, 18K, 14K)
- Historical price analysis
- Interactive price comparison charts
- Price trends visualization
- Automatic rate updates
- Price calculations per gram and 10 grams

## Requirements


Python 3.7+
streamlit
yfinance
pandas
plotly


## Installation

1. Clone the repository:
bash
git clone https://github.com/yourusername/gold-rate-tracker.git
cd gold-rate-tracker


2. Create and activate a virtual environment (optional but recommended):
bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate


3. Install the required packages:
bash
pip install -r requirements.txt


## Usage

1. Run the Streamlit application:
bash
streamlit run app.py


2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Price Calculations

The application calculates gold rates using:
- International market prices (from Yahoo Finance)
- Current USD-INR exchange rate
- Making charges (8%)
- Different purity conversions:
  - 24K: 99.9% pure gold
  - 22K: 91.6% pure gold
  - 18K: 75.0% pure gold
  - 14K: 58.5% pure gold

## Contributing

Feel free to fork the repository and submit pull requests for any improvements.

## License

MIT License - feel free to use this project for any purpose.
