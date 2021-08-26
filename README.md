# CheddarButler
Universal template for a fully automated financial trading program that is triggered by derivative functions of target source data.

//////General Structure of Program (GSP)//////

An initial "sell" script obtains the portfolio's balances and runs a historical analysis for each position held. From this analysis stocks that fit the condition to be sold are sent to a list that is run through a quote function, which is piped forward to a trade execution function that sells these positions.

<><><><>Sell
          Get balances
          Get historical Price Information
          Get quote
          Execute sale
<><><><>End

A second "buy" script instantiates a function to get the top moving stocks of the day. This array is further sliced by a desired price range and even volume threshold to generate a list of initial candidate financial symbols. From this list a dataframe of price history is generate, as well as historical option chains. From these two dataframes, which are the stock and option dataframes, quotes are retrieved for stocks that fall within certain parameters. For example, if a stock is trading above their target moving average, they would move on to be part of the list of candidate stocks to get quotes from. These quote candidates would then be pipe forward to the execution function to buy.

<><><><>Buy
          Get movers
          Get historical price information
          Get quote
          Execute sale
<><><><>End


/////Through The Barbed Wire//////




