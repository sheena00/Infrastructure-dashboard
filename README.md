# Infrastructure-dashboard
This project is an interactive dashboard built using streamlit and python. It uses Infrastructure and climate  indicators from the Formal Sector World Bank Enterprise Surveys (WBES). It covers different countries over different years . 
It includes:
- Filters for year and country 
- Ranked bar charts for selected indicators
- Indicator tables with wrapped headers
- Heatmaps showing relative performance

you can view the dashboard here: https://infrastructure-dashboard-wb.streamlit.app/

#structure of repository
Data - contains datasets
Data/clean contains datasets used by the dashboard
Scripts- contains my cleaning and dasboard scripts
requirements.txt contains all the packages required

#Using the dashboard
code: streamlit run dashboard.py
The dashboard will open in your browser
Use the filters on the left to filter by year and countries
The graphs , tables can be zoomed in and out

#Data sources
Word Bank enterprise survey datasets: https://www.enterprisesurveys.org/en/data
