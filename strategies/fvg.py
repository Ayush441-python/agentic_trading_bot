class FVG:

    @staticmethod
    def detect(df):

        gaps = []

        for i in range(2, len(df)):

            candle1_high = df["high"].iloc[i-2]
            candle3_low = df["low"].iloc[i]

            if candle3_low > candle1_high:

                gaps.append({
                    "type": "Bullish FVG",
                    "top": candle3_low,
                    "bottom": candle1_high,
                    "index": i
                })

            candle1_low = df["low"].iloc[i-2]
            candle3_high = df["high"].iloc[i]

            if candle3_high < candle1_low:

                gaps.append({
                    "type": "Bearish FVG",
                    "top": candle1_low,
                    "bottom": candle3_high,
                    "index": i
                })

        return gaps