import pandas as pd


class MarketStructure:

    @staticmethod
    def find_swings(df, lookback=3):

        swing_highs = []
        swing_lows = []

        for i in range(lookback, len(df)-lookback):

            high = df["high"].iloc[i]

            if high == max(
                df["high"].iloc[i-lookback:i+lookback+1]
            ):
                swing_highs.append(i)

            low = df["low"].iloc[i]

            if low == min(
                df["low"].iloc[i-lookback:i+lookback+1]
            ):
                swing_lows.append(i)

        return swing_highs, swing_lows
    
    @staticmethod
    def detect_bos(df, swing_highs, swing_lows):

        bos_signals = []

        for i in range(1, len(swing_highs)):

            prev_high = df["high"].iloc[
                swing_highs[i-1]
            ]

            curr_high = df["high"].iloc[
                swing_highs[i]
            ]

            if curr_high > prev_high:

                bos_signals.append({
                    "type": "Bullish BOS",
                    "price": curr_high,
                    "index": swing_highs[i]
                })

        for i in range(1, len(swing_lows)):

            prev_low = df["low"].iloc[
                swing_lows[i-1]
            ]

            curr_low = df["low"].iloc[
                swing_lows[i]
            ]

            if curr_low < prev_low:

                bos_signals.append({
                    "type": "Bearish BOS",
                    "price": curr_low,
                    "index": swing_lows[i]
                })

        return bos_signals