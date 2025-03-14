# E-Commerce Data Visualization Project

## Project Overview
This project involves creating data visualizations for e-commerce website data, analyzing user behavior, purchase patterns, and customer segmentation from October 2022 to February 2023.

## Exercise Directories
- ex00: Pie chart of site activity
- ex01: Time series and sales charts
- ex02: Statistical analysis and box plots
- ex03: Frequency and spending bar charts
- ex04: Cluster analysis planning (Elbow method)

## Requirements
- Python 3.x
- Required libraries: pandas, matplotlib, seaborn, scikit-learn

# Ex02 Statistical Analysis and Box Plots


The selected code shows how to create a horizontal boxplot visualization of average cart prices using matplotlib. 
## Boxplot Visualization

This boxplot will show the distribution of cart prices, highlighting the median, quartiles, range, and any potential outliers in the dataset.

Now I see what you were referring to! These are two different box plots from Exercise 02 ("My Beautiful Mustache") in your data visualization project.

### Describing 1st and 2nd graph price distribution

**Image 1:**
This is a box plot showing the distribution of individual item prices. The small diamond/dot shapes you were asking about are the outliers - individual data points that fall significantly outside the normal distribution range. In this case:

- The main box is quite narrow and centered around 0-50
- There are many outliers (the small dots) spread out to the right, going all the way to about 300
- There's even a small number of outliers on the negative side (around -50)
- This suggests that while most item prices are concentrated in a smaller range, there are some exceptionally expensive items and potentially some items with negative prices (possibly returns or discounts)

**Image 2:**
This is a box plot showing the average basket price per user, displayed with a green box:

- The box spans roughly from 2 to 6, meaning the middle 50% of average basket values fall in this range
- The vertical line inside the box (around 4) represents the median value
- The whiskers extend to about 0 on the left and 12 on the right
- This plot has no visible outliers, meaning all data points fall within the expected range

These visualizations help understand the price distributions in your dataset. The first plot shows there's a wide spread of individual item prices with many outliers, while the second suggests that when you look at customer averages, the spending patterns are more consistent with fewer extreme values.

### Describing 3th graph price distribution

This image shows a box plot, which is a simple way to visualize the distribution of numerical data.

In very easy terms:

- The blue box in the middle represents where the middle 50% of the data falls (between approximately 29 and 35)
- The orange vertical line inside the box shows the median (around 32), which is the middle value when all data is arranged in order
- The horizontal lines extending left and right (sometimes called "whiskers") show the range of the rest of the data that's not considered unusual
- The horizontal axis shows the values, ranging from about 26 to 42

This particular box plot appears to be showing the distribution of average spending or usage per customer, based on your earlier document. The fairly symmetric shape suggests a relatively normal distribution of values, with most customers having values between roughly 29 and 35.

This type of visualization is especially useful in Exercise 02 ("My Beautiful Mustache") from your project, where you need to display the distribution of prices or customer values to better understand their patterns.

# ex04 Frequency and Spending Bar Charts
# Visualization of Customer Frequency and Monetary Distribution

This code creates a side-by-side visualization of two key customer metrics using Matplotlib:

1. **Left Histogram**: Shows the frequency distribution of orders per customer
2. **Right Histogram**: Shows the monetary value distribution of purchases per customer

## Purpose:
This visualization allows analysis of customer behavior from two perspectives:
- **Purchase Frequency**: Identifies how frequently customers order
- **Purchase Value**: Shows spending distribution across customers

These metrics are foundational for customer segmentation (like RFM analysis) and can help identify high-value customers, occasional buyers, or other customer segments for targeted marketing.

# ex05 Cluster Analysis Planning (Elbow Method)
### Elbow Method for K-Means Clustering Explanation

 The Elbow Method helps decide how many groups (clusters) to use when training your K-Means clustering model.

Instead of guessing how many customer groups or segments exist in your data, the Elbow Method:

1. Tests different numbers of clusters (2 groups, 3 groups, 4 groups, etc.)
2. Measures how well each grouping fits your data
3. Shows you where adding more groups stops being helpful

It's like trying to divide customers into meaningful segments:
- Too few groups: you miss important differences
- Too many groups: you create artificial divisions that don't mean much

The "elbow" in the graph shows you the sweet spot - the optimal number of clusters for your specific data that balances simplicity with accuracy.

Here's what's happening step-by-step:

1. The code initializes an empty list called `wss` to store the Within-Cluster Sum of Squares values for different cluster counts.

2. It then loops through potential cluster counts from 1 to 9 (the range function goes up to but excludes 10).

3. For each value of K, it:
    - Creates a KMeans model with the specified number of clusters
    - Sets `random_state=0` for reproducibility of results
    - Uses `n_init=10` to run the algorithm 10 times with different centroid initializations, taking the best result
    - Fits the model to the provided data
    - Extracts the `inertia_` value, which is the sum of squared distances from each point to its assigned centroid
    - Appends this value to the `wss` list

4. Finally, it creates a line plot showing how the WSS decreases as the number of clusters increases, with:
    - The x-axis labeled "Number of clusters"
    - A title "The Elbow Method"
    - A display of the resulting plot

In an ideal scenario, the WSS plot will show a distinct bend or "elbow" where the rate of WSS reduction slows down. This point suggests the optimal number of clusters, as adding more clusters beyond this point provides only marginal improvement in cluster cohesion.

The resulting Elbow Method graph helps determine the optimal number of customer segments for the dataset. In a typical graph, you'll observe a steep decline initially (from 1 to 3 clusters), followed by a more gradual decrease. This characteristic "elbow" shape indicates where additional clusters provide diminishing returns. For e-commerce customer segmentation, around 3-4 clusters often represents an optimal balance between having distinct, meaningful customer groups while avoiding excessive fragmentation. This visualization directly supports Exercise 04's goal of determining appropriate customer segments for targeted email marketing campaigns.
