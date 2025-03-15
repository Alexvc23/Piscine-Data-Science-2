# Star Wars Knight Analysis Project

This project analyzes data from Star Wars knights to predict which side of the Force a knight belongs to. The goal is to determine if we could have predicted whether Anakin Skywalker would turn to the dark side based on his characteristics and skills.

## Project Overview

The dataset contains various knight attributes (features) and a target column "knight" that indicates whether the knight is a Jedi or Sith. Through data visualization, correlation analysis, and preprocessing techniques, we aim to understand what differentiates Jedi from Sith knights.

## Dataset

Two main datasets are used:
- `Train_knight.csv`: Contains knight data with labels (Jedi/Sith)
- `Test_knight.csv`: Contains knight data without labels

## Requirements

- Python 3.x
- pandas
- matplotlib
- numpy
- scikit-learn

## Exercise Solutions

### Exercise 00: Histogram Visualization (Histogram.py)

**Goal**: Create histograms to visualize the distribution of each feature in the test dataset, and compare feature distributions between Jedi and Sith knights in the training dataset.

**Solution**: 
The script creates two sets of histograms:
1. The first set displays the distribution of each feature in the test dataset
2. The second set shows the overlaid distributions for Jedi (blue) and Sith (red) for each feature in the training dataset

This visualization helps identify which features might have different distributions between Jedi and Sith, giving initial insights into potentially discriminative features.

The solution uses `matplotlib` to create a grid of histograms, using `subplot2grid` for layout control. The code efficiently processes each feature column to generate histograms with appropriate colors and labels.

### Exercise 01: Correlation Analysis (Correlation.py)

**Goal**: Determine which features have the strongest correlation with the knight type (Jedi/Sith).

**Solution**:
The script calculates correlation coefficients between the target variable (knight) and all features:
1. It first converts the categorical "knight" column to numeric (Jedi=1, Sith=0)
2. It then calculates the correlation matrix using pandas' `corr()` method
3. Finally, it sorts and prints the correlations with the "knight" column in descending order

The results show which features have the strongest positive or negative correlation with being a Jedi or Sith. This helps identify the most important features for predicting which side a knight belongs to.

According to your implementation, the highest correlations are with features like "Empowered", "Stims", "Prescience" and "Recovery", suggesting these are particularly important for distinguishing between Jedi and Sith.

To interpret correlation values:

- Values close to +1 indicate strong positive correlation (as one feature increases, the other tends to increase)
- Values close to -1 indicate strong negative correlation (as one feature increases, the other tends to decrease)
- Values close to 0 indicate little to no correlation (no consistent relationship)

For knight prediction, positive correlations suggest features more common in Jedi, while negative correlations suggest features more common in Sith. Features with correlation magnitudes above 0.5 (or below -0.5) are particularly useful for classification, while those close to zero provide little predictive power.

A heatmap visualization can also help identify relationships between features, with darker colors indicating stronger correlations.
### Exercise 02: Scatter Plot Analysis (points.py)

**Goal**: Create scatter plots to visualize the relationship between different features, with some plots showing separated clusters and others showing mixed clusters.

**Solution**:
The script generates four scatter plots:
1. Test dataset: Pull vs Push
2. Test dataset: Empowered vs Friendship
3. Training dataset: Empowered vs Friendship, color-coded by knight type (Jedi/Sith)
4. Training dataset: Pull/Push vs Friendship, color-coded by knight type (Jedi/Sith)

This allows for comparison between features that separate the knight types well and those that don't. The scatter plots help visualize which feature combinations might be useful for classification.

Your implementation uses different color schemes to distinguish between knight types (red for Sith, blue for Jedi, green for unknown knights in the test set) and creates a clean layout using `subplot2grid`.

### Exercise 03: Standardization (standardization.py)

**Goal**: Standardize the data (scale to zero mean and unit variance) and visualize the effect on the scatter plots.

**Solution**:
The script:
1. Loads both training and test datasets
2. Applies standardization using `StandardScaler` from scikit-learn
3. Creates scatter plots of standardized data for both datasets
4. Shows how the standardized Empowered vs Friendship features look for both datasets

This demonstrates how standardization affects the data distribution while preserving the separation between classes. Standardization is an important preprocessing step for many machine learning algorithms.

Your implementation correctly applies the standardization and recreates the scatter plots with the transformed data, allowing for comparison with the original plots.

### Exercise 04: Normalization (Normalization.py)

**Goal**: Normalize the data (scale to [0,1] range) and visualize the effect on scatter plots.

**Solution**:
The script:
1. Implements a custom normalization function that scales each feature to [0,1] range
2. Applies this normalization to both training and test datasets
3. Creates scatter plots similar to Exercise 02 but with normalized data

This shows how normalization affects the data distribution differently from standardization. Normalization is useful when features have different ranges and you want to bring them to a common scale.

Your custom `NormalizeMax` function performs min-max scaling, and the visualization demonstrates how the normalized features maintain relative relationships while being scaled to a common range.

### Exercise 05: Data Splitting (Normalization.py - second file)

**Goal**: Split the training dataset into training and validation sets.

**Solution**:
The script:
1. Loads the training dataset
2. Uses `train_test_split` from scikit-learn to split it into training (25%) and validation (75%) sets

This implements a common machine learning practice of setting aside a validation set to evaluate model performance before testing on unseen data.

Your implementation uses a 25% training / 75% validation split with a fixed random seed (42) for reproducibility, which allows for consistent results across different runs.

## Conclusions

Through these exercises, the project demonstrates:
1. Exploratory data analysis techniques
2. Feature correlation analysis
3. Data visualization techniques
4. Data preprocessing methods (standardization and normalization)
5. Dataset splitting for machine learning workflows

The analysis suggests that certain features like Empowered, Stims, Prescience, and Recovery have strong correlations with which side of the Force a knight belongs to. The visualizations demonstrate clear separation between Jedi and Sith knights when plotting certain feature combinations, indicating that it may indeed be possible to predict whether a knight like Anakin would tu 