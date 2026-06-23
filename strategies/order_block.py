class OrderBlock:

    @staticmethod
    def detect(df):

        order_blocks = []

        for i in range(1, len(df)-1):

            current = df.iloc[i]

            next_candle = df.iloc[i+1]

            # Bullish OB

            if (
                current["close"] < current["open"]
                and
                next_candle["close"] >
                current["high"]
            ):

                order_blocks.append({
                    "type": "Bullish OB",
                    "high": current["high"],
                    "low": current["low"],
                    "index": i
                })

            # Bearish OB

            if (
                current["close"] > current["open"]
                and
                next_candle["close"] <
                current["low"]
            ):

                order_blocks.append({
                    "type": "Bearish OB",
                    "high": current["high"],
                    "low": current["low"],
                    "index": i
                })

        return order_blocks