# Charlie Bear Details Grabber

An extremely bare-bones (mind the pun) Selenium-based webscraper that obtains details about Charlie Bears from the Charlie Bear "Bear Library" and exports them in a JSON format. 

# Getting Started 

## Python Libraries

Firstly, install the required Python libraries using pip from your working directory:

```
pip install -r requirements.txt
```

**N.B.** It is highly recommended that you create a [Python Virtual Environment](https://docs.python.org/3/library/venv.html) before installing these libraries to prevent incompataibilty issues.

# Running the Program 
Once you have your requirements, or have set up a Virtual Environment, you can run the program as below:

```
python main.py
```

This will download the latest ChromeDriver to your device, open it to the Bear Library, and begin to scrape data. 

**_n.b._** There are a _lot_ of Charlie Bears and this script does take quite a while to finish. Please be patient!

# Viewing the Output
Once the program has successfully finished running, a file named `output.json` will be generated in your working directory.

This file contains a list of JSON objects containing basic details about each Bear Collection, and the bears within it. 

![Screenshot of the output.json file, containing details for the Bear known as "Adelaide".](https://i.imgur.com/P6VKzcD.png "An example collection / bear object.")

## Disclaimer 
This tool is not affiliated with, or authorised by, Charlie Bears. I make no claim to any of the data that this tool exports.