from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field

import yfinance as yf


class StockDataToolInput(BaseModel):
    """Input schema for StockDataTool."""
    stock: str = Field(..., description="The stock ticker symbol to fetch data for.")

class StockDataTool(BaseTool):
    name: str = "Stock Data Fetcher"
    description: str = (
        "Fetches historical stock data for a given ticker symbol using Yahoo Finance API"
    )
    args_schema: Type[BaseModel] = StockDataToolInput
    # stock: Optional[str] = None

    def __init__(self, stock: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        # self.stock = stock
        # content = self.fetch_stock_data(stock)
        # self.add(content)

    def fetch_stock_data(self, stock: str) -> Optional[dict]:
        """Fetch historical stock data for the specified ticker symbol."""
        try:
            ticker = yf.Ticker(stock)
            historical_data = ticker.history(period='1mo')
            return historical_data.to_dict()
        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")
            return None

    def _run(self, stock: str) -> dict:
        return self.fetch_stock_data(stock)
