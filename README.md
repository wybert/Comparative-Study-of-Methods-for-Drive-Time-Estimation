Comparative-Study-of-Methods-for-Drive-Time-Estimation
==============================

Code for FOSS4G 2023, start with the notebooks under notebooks folder.

Project Organization
```bash
├── LICENSE
├── Makefile
├── README.md
├── data
│   ├── external
│   ├── interim
│   ├── processed
│   │   └── sample_and_results.csv
│   └── raw
│       └── cb_2018_us_state_500k.zip
├── data_sync.py
├── docs
│   ├── Makefile
│   ├── commands.rst
│   ├── conf.py
│   ├── getting-started.rst
│   ├── index.rst
│   └── make.bat
├── models
├── notebooks
│   ├── 0.1-xiaokang-routing-calculation.ipynb
│   └── 0.2-xiaokang-results-visualization.ipynb
├── references
├── reports
│   └── figures
│       └── Comparison_of_Route_Drive_Durations.png
├── requirements.txt
├── setup.py
├── src
│   ├── __init__.py
│   ├── data
│   │   ├── __init__.py
│   │   └── make_dataset.py
│   ├── features
│   │   ├── __init__.py
│   │   └── build_features.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── cal_osmnx.py
│   │   ├── predict_model.py
│   │   └── train_model.py
│   └── visualization
│       ├── __init__.py
│       └── visualize.py
├── test_environment.py
└── tox.ini
```
[Here is the script](https://github.com/wybert/Comparative-Study-of-Methods-for-Drive-Time-Estimation/blob/main/src/google_distance_matrix_20231006.py) for the routing calculation using Google Maps API





<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
