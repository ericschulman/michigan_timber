# Overview

I use the [Vuong (1989)](https://www.jstor.org/stable/1912557) test to understand how bidders decide whether to enter into auctions. The main datasets and anaylsis is in the `mich_data` which are data from Michigan Timber auctions scraped directly from the website. This setting is similar to [Li and Zheng (2012)](https://www.sciencedirect.com/science/article/pii/S0304407611001679), who test to see whether there is a selection bias among observed bids.   There is also a folder with `cal_data` which are auctions for california highway contracts.  Not all bidders submit bids and there is a missing data problem.


# Testing Procedure

The main testing module is `vuong_tests.py`. For more information on the testing procedure see [this](https://github.com/ericschulman/testing) or [this](https://github.com/ericschulman/testing_empirical_ex) repository. I use a similar methodology to that in my [job market paper](https://drive.google.com/file/d/14FdLzfvJzOyyH0F6itTg2TeE7dgiF9Jd/view)
 
* Model 1: To estimate the bidding distribution, I would regress bids on auction and bidder characteristics with OLS on the complete cases.
* Model 2: To approximate the bidding distribution, I would use a Tobit to control for selection bias.
* I select between models using the bootstrapped Vuong test.

In this context, a selection bias says that bidders entering have relatively higher valuations than bidders who do not enter the auction. As a result, a selection bias among bids would increase optimal reserve prices as shown by [Gentry and Li (2014)](https://onlinelibrary.wiley.com/doi/abs/10.3982/ECTA10293). If there is a selection bias, then bidders have more private information and there are more opportunities to extract information rents from the seller.


# Michigan data

The Michigan data is similar to that of [Li and Zheng (2012)](https://www.sciencedirect.com/science/article/pii/S0304407611001679). The Michigan Department of Natural Resources (MDoNR) sells standing timber through the standard first-price, sealed-bid auctions with a public reserve price. All bids are collected simultaneously. The lot is sold to the Winbid bidder who pays his bid to the state government.   I focus on the data from the Baldwin field office.  I obtained this data from the MDoNR website which is freely available and posted to an https server. This state agency is in charge of the management of state forests in Michigan. The  MDoNR provides very detailed information concerning the timber, such as the various species in the lot, the volumes of each species, the percentage of saw timber and the minimum acceptable bid (the public reserve price). My data is from January 2005 to August of 2012. I have data on 306 auctions with 1172 total bids. 


* `mich_scrape` contains the code for the scrape. `scrape.sh` contains the actual scraper. Once the code is scraped `create_sales.ipynb` and `create_bids.ipynb` contain the code for turning the directory structure into a usable `.csv file`
* `merged_data` merges the sales data with the open bid data into one file which can be used for analysis.
* There is a readme in the `mich_data` folder which explains the key variables.
* The file `mich_data/create_panel.py` creates a balanced panel from the scrapped data. This panel can be used to run the analysis.
* A similar dataset was used by [this](https://www.sciencedirect.com/science/article/pii/S0304407611001679) paper.

In the timber auctions considered, there is no pre-determined list of bidders. Most bidders submit less than 1 bids per month. As a result, the pool of potential bidders with missing bids appears random. 

# California data

The California data is replication data from [this](https://www.aeaweb.org/articles?id=10.1257/aer.101.6.2653) paper. The folder contains a description of the variables.
