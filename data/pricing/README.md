# Agmarknet

This public repository contains data relating to Indian wholesale food markets. It contains about 4 million data points relating to 12 food products during the period 2008 through June 2017.

## Data source

The data was downloaded from a website maintained by the Indian government (in particular, the Directorate of Marketing and Inspection). The website is located here: http://agmarknet.gov.in/

## Format

For each crop (e.g. rice, maize, soybean), the data is split such that there is one CSV file per year. Each row contains a summary of sales for that crop in a given market on a given day.

The names of the columns, as defined by the Agmarknet website, are: 'State Name', 'District Name', 'Market Name', 'Variety', 'Group', 'Arrivals (Tonnes)', 'Min Price (Rs./Quintal)', 'Max Price (Rs./Quintal)', 'Modal Price (Rs./Quintal)', 'Reported Date'.

## How it was obtained

I downloaded the data in June 2017. At this time (July 6th, 2017) it's not possible to download more than one day's data at once. To cope with this I used the Python packages Mechanize and BeautifulSoup and deployed a script on Google Cloud.

The repository is not being continually updated with new data.
