import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1️⃣ Data Collection ---
print("--- 1️⃣ Data Collection ---")
data_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

try:
    df = pd.read_csv(data_url)
    print("Data successfully loaded from Our World in Data!")
except Exception as e:
    print(f"Error loading data: {e}")
    print("Please ensure you have a stable internet connection or download the CSV manually.")
    # If download fails, you might want to include a fallback to a local file
    # df = pd.read_csv('owid-covid-data.csv')
    exit()

# --- 2️⃣ Data Loading & Exploration ---
print("\n--- 2️⃣ Data Loading & Exploration ---")

# Check columns
print("\nColumns in the dataset:")
print(df.columns)

# Preview first few rows
print("\nFirst 5 rows of the dataset:")
print(df.head())

# Identify missing values
print("\nNumber of missing values per column:")
print(df.isnull().sum())

# --- 3️⃣ Data Cleaning ---
print("\n--- 3️⃣ Data Cleaning ---")

# Filter countries of interest
countries_of_interest = ['Kenya', 'United States', 'India']
df_filtered = df[df['location'].isin(countries_of_interest)].copy()
print(f"\nData filtered for: {countries_of_interest}")

# Drop rows with missing dates (critical)
df_filtered.dropna(subset=['date'], inplace=True)
print(f"\nNumber of rows after dropping missing dates: {len(df_filtered)}")

# Convert date column to datetime
df_filtered['date'] = pd.to_datetime(df_filtered['date'])
print("\n'date' column converted to datetime.")

# Handle missing numeric values (example: filling with 0 or interpolating)
numeric_cols = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'total_vaccinations', 'new_vaccinations']
for col in numeric_cols:
    df_filtered[col].fillna(0, inplace=True) # Filling with 0 for simplicity
print("\nMissing numeric values filled with 0.")

print("\nFirst few rows of the cleaned and filtered data:")
print(df_filtered.head())

print("\nNumber of missing values after cleaning:")
print(df_filtered.isnull().sum())

# --- 4️⃣ Exploratory Data Analysis (EDA) ---
print("\n--- 4️⃣ Exploratory Data Analysis (EDA) ---")

# Set 'date' as index for time series analysis
df_filtered.set_index('date', inplace=True)

# Plot total cases over time for selected countries
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data.index, country_data['total_cases'], label=country)
plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot total deaths over time
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data.index, country_data['total_deaths'], label=country)
plt.title('Total COVID-19 Deaths Over Time')
plt.xlabel('Date')
plt.ylabel('Total Deaths')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Compare daily new cases between countries
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data.index, country_data['new_cases'], label=country)
plt.title('Daily New COVID-19 Cases')
plt.xlabel('Date')
plt.ylabel('New Cases')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Calculate the death rate (total_deaths / total_cases)
df_filtered['death_rate'] = df_filtered['total_deaths'] / df_filtered['total_cases']

plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data.index, country_data['death_rate'], label=country)
plt.title('COVID-19 Death Rate (Total Deaths / Total Cases)')
plt.xlabel('Date')
plt.ylabel('Death Rate')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

print("\n--- EDA Completed ---")