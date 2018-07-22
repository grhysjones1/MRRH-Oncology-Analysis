# MRRH-Oncology-Analysis

# This repository stores the python scripts used to analyse cancer records collected from Mbarara Regional Referral Hospital in Uganda

# There are 9 key scripts:
# 0. Data Preparation - reads in CSV data, formats, and re-orders the dataset. Defines major cancer types to examine
# 1. Cancers by Year - counts the number of different (major) cancer types by year and month and plot on line graph
# 2. Other Cancer Analysis - looks for information in the 'Other' cancers field, to extract as much data as possible on cancer types
# 3. Age Analysis - buckets patients by age and plots differences in age profile by major cancer type
# 4. Gender Analysis - plots the gender split by major cancer type
# 5. District Breakdown - cleans district data, shows the overall district breakdown and looks for changes in districts served across years
# 6. Chemotherapy Analysis - analyses the usage of difference chemotherapy regimens by major cancer type
# 7. Data Completeness - looks at the completeness of each variable in the dataset to understand how well data is being captured by clinicians
