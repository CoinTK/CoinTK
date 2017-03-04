# TODO List

* General

	- [ ] Document all the function input parameters


* Dry testing

	- [ ] In addition to running our strategies on past data, we want to be able to pull live data (syncing with Bitcoin trading APIs) and dry-run our algorithms, so users can see the performance of their own strategies live.
	- [ ] Support for pulling data from multiple exchanges (but still running single-exchange strategies)
	- [ ] Support for multi-exchange strategies


* Better Strategies

	- [ ] Auto-compare strategies by running them with the same seeding multiple times and comparing results
	- [ ] Machine Learning, especially to predict prescient algorithms
		- [ ] General framework for a ML training interface
	- [ ] Clean up EMA code logic & optimize its parameters
		- [ ] Think more about its logic -- maybe 'order_once' should take into consideration the trend_threshold as well; 'follow_trend': trend detection should be less sharp and more forgiving; maybe qty=-1 isn't ideal (maybe it should scale with the trend?)
	- [ ] Higher-performing strategies
	- [ ] General framework for risk management of strategies


* Performance Visualization & Evaluation

	- [ ] Ability to graph multiply strategies in the same graph (run multiple backtests for the same graph)


* Live Testing

	- [ ] Live connection to the exchanges, being able to run strategies real-time with real-money.
