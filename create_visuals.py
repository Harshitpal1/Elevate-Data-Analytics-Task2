import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuration: Set a professional plot style and color palette ---
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('viridis')

def load_and_prepare_data(filepath: str) -> pd.DataFrame:
    """
    Loads and prepares the Superstore dataset from a CSV file.

    Args:
        filepath (str): The path to the Superstore.csv file.

    Returns:
        pd.DataFrame: A prepared Pandas DataFrame, or None if the file is not found.
    """
    try:
        df = pd.read_csv(filepath, encoding='windows-1252')
        # Convert 'Order Date' to datetime objects for time-series analysis
        df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
        print("✅ Dataset loaded and prepared successfully.")
        return df
    except FileNotFoundError:
        print(f"❌ Error: The file '{filepath}' was not found.")
        return None

def plot_sales_and_profit_over_time(df: pd.DataFrame):
    """Generates and saves a line chart of monthly sales and profit."""
    print("Generating Chart 1: Monthly Sales and Profit...")
    monthly_data = df.set_index('Order Date').resample('M').agg({'Sales': 'sum', 'Profit': 'sum'})

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(monthly_data.index, monthly_data['Sales'], label='Total Sales', color='royalblue', linewidth=2.5)
    ax.fill_between(monthly_data.index, monthly_data['Profit'], color="skyblue", alpha=0.4, label='Total Profit')

    ax.set_title('Monthly Sales and Profit Over Time (2014-2017)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Amount (USD)', fontsize=12)
    ax.legend()
    fig.tight_layout()
    plt.savefig('1_sales_profit_over_time.png', dpi=300)
    print("✅ Chart 1 saved.")

def plot_sales_by_subcategory(df: pd.DataFrame):
    """Generates and saves a bar chart of sales by product sub-category."""
    print("Generating Chart 2: Sales and Profit by Sub-Category...")
    subcat_data = df.groupby('Sub-Category').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values('Sales', ascending=False)

    fig, ax = plt.subplots(figsize=(12, 10))
    colors = ['tomato' if p < 0 else 'mediumseagreen' for p in subcat_data['Profit']]
    sns.barplot(x=subcat_data['Sales'], y=subcat_data.index, palette=colors, ax=ax)

    ax.set_title('Sales Performance by Product Sub-Category', fontsize=16, fontweight='bold')
    ax.set_xlabel('Total Sales (USD)', fontsize=12)
    ax.set_ylabel('Product Sub-Category', fontsize=12)
    fig.tight_layout()
    plt.savefig('2_sales_by_subcategory.png', dpi=300)
    print("✅ Chart 2 saved.")

def plot_sales_by_segment(df: pd.DataFrame):
    """Generates and saves a bar chart of sales by customer segment."""
    print("Generating Chart 3: Sales by Customer Segment...")
    segment_sales = df.groupby('Segment')['Sales'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=segment_sales.index, y=segment_sales.values, ax=ax)

    ax.set_title('Total Sales by Customer Segment', fontsize=16, fontweight='bold')
    ax.set_xlabel('Customer Segment', fontsize=12)
    ax.set_ylabel('Total Sales (USD)', fontsize=12)
    fig.tight_layout()
    plt.savefig('3_sales_by_segment.png', dpi=300)
    print("✅ Chart 3 saved.")

def main():
    """Main function to run the data visualization script."""
    print("--- Starting Superstore Data Visualization Script ---")
    
    # Define the path to your dataset
    dataset_path = 'Superstore.csv'
    
    # Load and prepare the data
    superstore_df = load_and_prepare_data(dataset_path)
    
    # Proceed only if the data was loaded successfully
    if superstore_df is not None:
        # Generate and save all visualizations
        plot_sales_and_profit_over_time(superstore_df)
        plot_sales_by_subcategory(superstore_df)
        plot_sales_by_segment(superstore_df)
        print("\n🚀 All visualizations have been generated and saved as PNG files.")
    else:
        print("\nScript terminated due to data loading error.")

# --- This ensures the main function runs only when the script is executed directly ---
if __name__ == "__main__":
    main()
