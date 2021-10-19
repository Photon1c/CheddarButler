Welcome to the CheddarButlerTutorial. Click Start to begin the tutorial.

Introduction

CheddarButler is an app that automates trading or can be set up to be purely
informational, with no broker information entered. To start the basic tutorial run the following command in the terminal while inside the documentation directory:


cloudshell launch-tutorial -d tutorial.md

The advanced setup tutorial can be accessed by entering the following command in the terminal while inside the documentation directory:


cloudshell launch-tutorial -d advancedtutorial.md


Initial Configutation

The config.py file contains the keys that the program will need to run, whether these are Ameritrade, Alpaca or other API keys.

The Sell Function

Assuming that CheddarButler is set up for broker usage the sell function can retrieve current portfolio balances, and run a similar version of the buy stocks function. Historical stock information is obtained for each stock owned, quotes are retrieved for those target symbols making the cut, and a sell function is constructed to exit these  undesirable positions.

<walkthrough-editor-open-file
    filePath="/home/lescua/projects/fin_suite/CheddarButler_v1/app/sell.py">
    open sell.py
</walkthrough-editor-open-file>



The Buy_Stocks Function

Historical stock information can be obtained either through yahoo finance, or directly from
brokers like TD Ameritrade or Alpaca that have been configured to connect through their
respective authentication protocols. Each of them is specific to each broker, for more 
information on how to set these up please check out the advanced tutorial. For this section
a general description of the non-broker linked app follows.

Stocks and their symbols can be collected into a list that can either be further saved as a csv file or kept as a list object in the program. The way the program is set up is such that 
a csv file is created so that the next step can call the file, but further configuration of this could include simply callin the list object without having to write and read to and from
these csv files, which are saved in the csvs folder. The purpose of this is for user friendliness- this way tickers can be manually added to the file, or the file can be analyzed
and copied to new files which serve different purposes. 

The buy stocks function initializes with getting the historical stock information for each of
these tickers on the defined list. It can be set up so that it obtains a desired number of months going back. The default number of period months is set to 1. Additionally the moving
average conditional variable is set to 10 days by default, but can be adjusted to the desired
value.

One the historical price information is retrieved, dataframes are constructed using pandas to sort through the data and compare to the newly created column- the N day moving average. A final list is constructed from these initial dataframes that only contains target symbols that are candidates to be bought.

The target symbols are entered into a quote function to obtain the lastest ask price, and
the buy execution function is constructed and passed.

It should be mentioned that the buy_stocks function imports the portfolio and cash balance from the sell function in order to compute the quantity of stocks to buy. By default two conditions must be met in order for the buy_stocks function to run: 

1.- cash in portfolio must make up no less than 75% by default, this value can be changed.

2.- the quantity of stock to buy is equal to the desired holding percentage (i.e no more
than 15% of the stock should make up the total portfolio), multiplied by the portfolio 
balance divided by the price. This naturally follows the [PQ]/portfolio < .15 boolean
conditional.


The Buy_Options function

Similar to the buy stocks function, this portion of the program consists of three basic steps.

The first step is to import the target symbols from the buy stocks function, the second to get option chain data for the defined number of periods, constructing dataframes that filter and sort through the desired ask prices.
Finally the third is to execute a buy functon for those options that meet the conditions.
