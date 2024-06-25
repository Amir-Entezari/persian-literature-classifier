
# Persian Author Classification

## Project Overview
This project aims to classify texts by various Persian authors using machine learning techniques. The goal is to accurately predict the author of a given text based on its content.

## Models and Techniques
- **Text Preprocessing**: Tokenization, normalization, and vectorization of Persian text.
- **Machine Learning Models**: Utilization of models such as SVM, Naive Bayes, and Random Forest for classification.
- **Evaluation**: Accuracy, Precision, Recall, and F1 Score metrics are used to evaluate the models.

## Results
The project achieved an accuracy of 70% on the testing set, with detailed performance metrics available in the `report.pdf`.

## Repository Contents
- `persian_authors_classification.ipynb`: Jupyter notebook with the main classification algorithms and model evaluations.
- `scrapper.ipynb`: Jupyter notebook used for scraping textual data from various online sources.
- `report.pdf`: A comprehensive report detailing the methodology, analysis, and results of the project.
- `src/`: Directory containing additional source code and utility scripts supporting the project.

## Installation
To set up the project environment:

```bash
git clone https://github.com/Amir-Entezari/persian-literature-classifier.git
cd persian_author_classification
pip install -r requirements.txt
```

## Usage
To run the classification notebook:

```bash
jupyter notebook persian_authors_classification.ipynb
```

To execute the scraper:

```bash
jupyter notebook scrapper.ipynb
```

## Contribution
Contributions to the project are welcome. To contribute, please fork the repository, make your changes, and submit a pull request.

## Contact
For questions or feedback, please open an issue in the GitHub repository or contact amirh.entezari@ut.ac.ir .
