# BattleLogAnalyzer

A unique approach to store and analyse your Brawl Stars Battle Logs constantly!
More features coming soon! PRs are encouraged but the automatic workflow is not done yet so expect some delays to get it merged.

## How to use

- Get your API token from the [Brawl-Stars Developer Portal](https://developer.brawlstars.com). It is IP locked so make sure you have proper arrangements!
- Paste it in the `token.env.example` file for your environment and rename it to `token.env`. Also read the FAQ before using it.
- Install the requirements using the `requirements.txt` file.
- The `store.py` script saves the battle logs to a python shelve and the `read.py` file analyzes the logs and gives a report. The `continuous_store.py` and the `continuous_read.py` files are self explanatory!

## FAQs

1. Can I run it on both Windows and Unix based systems? Simultaneously?

> Yes and No! Unfortunately the way shelve handles the local databases and how the automated running of python script works are platform dependant. You cannot update the files of one OS variant with another. However, if you are on Windows, you can use Windows Subsystem for Linux and use the Unix based script. It would work like a charm. I will look into reliably storing the data using some other way soon.

2. It is using the Brawlstats package, can I use the `BrawlAPI` instead of the `OfficialAPI`?

> As the Official API is only supported by Supercell, I would only attend to issues regarding to it. You can however try anything as long as you are not violating the terms of service of supercell.

3. I have custom python environments set up. How do I use the `continuous_*.py` scripts with it?

> Those are just subprocess calls. You can modify it as per your requirement.

4. The update time is too slow for me what do I do?

> Just edit the `continuous_*.py` files and change the `time.sleep()` function's arguments. 15 Minutes is fine for a casual player. Maybe add a PR with a `.env` integration if you want! *wink wink*
