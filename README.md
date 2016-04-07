# Austin campaign finance scraper
A Fabric script to scrape City of Austin campaign finance reports (PDFs + metadata).

### Requirements
```
virtualenv
pip
```

### Setup
Clone this repo, activate the virtual environment, install the requirements.
```shell
$ git clone git@github.com:statesman/austin-campaign-finance-scraper.git
$ cd austin-campaign-finance-scraper
$ source bin/activate
$ pip install -r requirements.txt
```

### Run the script
```shell
$ fab scrapeEm
```

### Results
After running the script, you should end up with:
1. A directory for each year, 2009-2016, each containing PDF scans of campaign finance reports for that year. Reports are slugged `{year}-{month}-{day}-{filer_name}.pdf`. Corrected reports are slugged `{year}-{month}-{day}-{filer_name}-corrected.pdf`.
2. A JSON metadata file.
3. A zipfile containing (1) and (2).

### Todo
Refactor for DRY-ness.
