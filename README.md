# Find Tatooine

A Streamlit conversion of the exoplanet notebook, redesigned as a guided data-science investigation rather than a Python-coding lesson.

## Run locally on Windows CMD

```cmd
conda activate exoplanets-streamlit
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## App stages

1. Meet the data and inspect missing values.
2. Explore discoveries by year and method.
3. Compare exoplanet properties interactively.
4. Convert the description of Tatooine into adjustable filters.
5. Map the selected candidate using right ascension and declination.

The app first tries to retrieve selected fields from the NASA Exoplanet Archive. If the request fails, use the bundled notebook sample from the sidebar.
