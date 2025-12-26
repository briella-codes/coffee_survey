# COFFEE SURVEY ANALYSIS (Work IN PROGRESS: this project is still being developed and improved)
**Being programmer and coffee lover** like many other programmers, I choose this project to combine **my passion for coding** with exploring coffee consumption habits through data analysis, while demonstrating data cleaning, transformation and exploratory data analysis skills using **Pyhton, Pandas, MatPlotLib and regex**

**Original CVS source:** public major coffee survey from James Hoffmann, "Great American Taste Test"
**Type:**  56 questions answered by 4,042 participants, survey data with mixed data types, multi-value, categorical, ranges-based purposes ...
Dataset used for educational purposes.

## HOW TO RUN THE PROJECT
GoogleColab: Open the notebook and run all the cells <br>
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/briella-codes/coffee_survey/blob/main/notebooks/survey_analysis.ipynb)  <br>
Click here to open in GoogleColab: <br>
[https://colab.research.google.com/github/briella-codes/coffee_survey/blob/main/notebooks/survey_analysis.ipynb](https://colab.research.google.com/github/briella-codes/coffee_survey/blob/main/notebooks/survey_analysis.ipynb)


## DATA PROCESSING
- Standardization of diferents types of values  <br>
- Cleaning and **normalization** of *range-based responses* (age, cups, spending...)  <br>
- Use of **Regular Expressions (regex)** for extracting and cleaning text-based data
- **Detecting and handling of missing or null values**
- Correction of data types
- Normalization and scaling of numeric values
- Creating of **new features / columns for clusteringor further analysis** (min/max columns, etc)   <br>
- Exporting cleaned and processed dataset as new CSV file

## ANALYSIS HIGHTLIGHTS
- Percentage of coffee consumers by age group  <br>
-  Number of consumers grouped and counted by additives(sugar, milk, syrup, etc) and by age group  <br>
- Sweetener usage by age group (and by educational level)  <br>
- Hight-consumption consumer profiles *(in progress)*  <br>
- Spending behavior  *(in progress)* <br>

## TOOLS:
- Python  <br>
- Pandas  <br>
- MatPlotLib  <br>

## STRUCTURE:
```data/raw``` : original csv file  <br>
```data/processed```: cleaned datasets  <br>
```src```: python data cleaning functions  <br>
```notebooks``` : exploratory analysis and pie chart and bar charts visualizations using functions





