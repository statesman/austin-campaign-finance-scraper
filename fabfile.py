import requests
import json
from bs4 import BeautifulSoup
import time
from fabric.operations import local
from slugify import slugify


def scrapeEm():
    """This works but needs refactoring for DRY-ness"""

    # pages with newer CSS
    new_style_page_list = (
        "http://austintexas.gov/cityclerk/elections/2016_campaign_finance_reporting.htm",
        "http://austintexas.gov/cityclerk/elections/2015_campaign_finance_reporting.htm",
        "http://austintexas.gov/cityclerk/elections/2014_campaign_finance_reporting.htm",
        "http://austintexas.gov/cityclerk/elections/2013_campaign_finance_reporting.htm",
        "http://austintexas.gov/cityclerk/elections/2012_campaign_finance_reporting.htm",
    )

    # pages with old CSS
    old_style_page_list = (
        "http://austintexas.gov/cityclerk/elections/2011_campaign_finance_reporting.htm",
        "http://austintexas.gov/cityclerk/elections/2010_Campaign_Finance_Reports.htm",
        "http://www.austintexas.gov/cityclerk/elections/2009_Campaign_Finance_Reports.htm",
    )

    # list to append things to
    outlist = []

    # scrape the new-style pages
    for page in new_style_page_list:
        r = requests.get(page)
        soup = BeautifulSoup(r.text, "html.parser")
        trs = soup.find_all("tr", {"bgcolor": "#ffffff"})
        for row in trs:
            record = {}
            col = row.find_all('td')

            filer = col[0].p.string.strip()
            print("pulling data for " + filer)
            record['filer'] = filer

            record['reports'] = []
            reports = col[1].find_all("a")
            for i, report in enumerate(reports):
                rep = {}
                pdf = report['href']
                file_date = report.string.strip().split("/")
                file_year = file_date[-1]
                local("mkdir -p " + file_year)
                file_month = '{:02d}'.format(
                    int(file_date[0].strip())
                )
                file_day = '{:02d}'.format(
                    int(file_date[1].strip())
                )
                file_date = "-".join([file_year, file_month, file_day])
                slugname = (file_date + "-" + slugify(filer.lower()) +
                            "-" + str(i) + ".pdf")
                local("wget -O " + file_year + "/" + slugname +
                      " " + pdf, capture=False)
                rep['file_name'] = slugname
                rep['file_date'] = file_date
                record['reports'].append(rep)

            # check for corrected reports
            corrected_reports = col[2].find_all("a")
            if len(corrected_reports) > 0:
                record['corrected_reports'] = []
                for i, c_report in enumerate(corrected_reports):
                    rep = {}
                    pdf = c_report['href']
                    file_date = c_report.string.strip().split("/")
                    file_year = file_date[-1]
                    file_month = '{:02d}'.format(
                        int(file_date[0].strip())
                    )
                    file_day = '{:02d}'.format(
                        int(file_date[1].strip())
                    )
                    file_date = "-".join([file_year, file_month, file_day])
                    slugname = (file_date + "-" + slugify(filer.lower()) +
                                "-corrected-" + str(i) + ".pdf")
                    local("wget -O " + file_year + "/" + slugname +
                          " " + pdf, capture=False)
                    rep['file_name'] = slugname
                    rep['file_date'] = file_date
                    record['corrected_reports'].append(rep)
            outlist.append(record)
        time.sleep(1)

    # scrape old-style pages
    for page in old_style_page_list:
        r = requests.get(page)
        soup = BeautifulSoup(r.text, "html.parser")
        trs = soup.find_all("tr", {"valign": "middle"})
        for row in trs:
            record = {}
            col = row.find_all('td')

            filer = col[0].p.string.strip()
            print("pulling data for " + filer)
            record['filer'] = filer

            record['reports'] = []
            reports = col[1].find_all("a")
            for i, report in enumerate(reports):
                rep = {}
                pdf = report['href']
                file_date = report.string.strip().split("/")
                file_year = file_date[-1]
                local("mkdir -p " + file_year)
                file_month = '{:02d}'.format(
                    int(file_date[0].strip())
                )
                file_day = '{:02d}'.format(
                    int(file_date[1].strip())
                )
                file_date = "-".join([file_year, file_month, file_day])
                slugname = (file_date + "-" + slugify(filer.lower()) +
                            "-" + str(i) + ".pdf")
                local("wget -O " + file_year + "/" + slugname +
                      " " + pdf, capture=False)
                rep['file_name'] = slugname
                rep['file_date'] = file_date
                record['reports'].append(rep)

            # check for corrected reports
            corrected_reports = col[2].find_all("a")
            if len(corrected_reports) > 0:
                record['corrected_reports'] = []
                for i, c_report in enumerate(corrected_reports):
                    rep = {}
                    pdf = c_report['href']
                    file_date = c_report.string.strip().split("/")
                    file_year = file_date[-1]
                    file_month = '{:02d}'.format(
                        int(file_date[0].strip())
                    )
                    file_day = '{:02d}'.format(
                        int(file_date[1].strip())
                    )
                    file_date = "-".join([file_year, file_month, file_day])
                    slugname = (file_date + "-" + slugify(filer.lower()) +
                                "-corrected-" + str(i) + ".pdf")
                    local("wget -O " + file_year + "/" + slugname +
                          " " + pdf, capture=False)
                    rep['file_name'] = slugname
                    rep['file_date'] = file_date
                    record['corrected_reports'].append(rep)
            outlist.append(record)
        time.sleep(1)

    # write the results to a json file
    with open("austin_finance_reports_metadata.json", "wb") as jsonout:
        jsonout.write(json.dumps(outlist))

    # zip it up
    local("zip austin_finance_reports.zip austin_finance_reports_metadata.json */*")
