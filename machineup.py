import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import warnings
warnings.filterwarnings("ignore")

def plot_and_save_to_pdf(df, user_date, pdf_pages):
    print("Creating pdf for : ",user_date)
    # Filter the DataFrame for the provided date
    filtered_df = df[df['timestamp'].dt.date == pd.to_datetime(user_date).date()]

    filtered_df['hour'] = filtered_df['timestamp'].dt.hour
    hourly_running_time = filtered_df.groupby('hour')['timestamp'].count()

    # Convert the count to minutes
    hourly_running_time = hourly_running_time

    hourly_running_time = hourly_running_time.where(hourly_running_time <= 60, 60)

    # Plot the machine running time for each hour
    plt.figure(figsize=(15, 8))
    bars = plt.bar(hourly_running_time.index, hourly_running_time.values)

    for bar in bars:
        height = min(bar.get_height(), 60)  # Limit the label to 60 if greater
        plt.annotate(f'{height:.2f}',  # Format the annotation as a floating-point number with 2 decimal places
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),  # Offset the text slightly above the bar
                     textcoords='offset points',
                     ha='center', va='bottom')

    # Customize the plot
    plt.title(f'Uptime Status for Date: {user_date}')
    plt.xlabel('Time of the day (Hour)')
    plt.ylabel('Running Time (minutes)')
    plt.xticks(range(24))
    plt.ylim(0, 70)

    # Save the plot to the PDF page
    pdf_pages.savefig()
    plt.close()  # Close the plot to release resources

def main():
    # Read the CSV file into a DataFrame
    df = pd.read_csv('log.csv')

    # Convert the timestamp column to a datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Get unique dates in the DataFrame
    unique_dates = df['timestamp'].dt.date.unique()

    # Create a PDF file to store the plots
    with PdfPages('machine_uptime_summary.pdf') as pdf:
        # Iterate through unique dates and create plots
        for date in unique_dates:
            user_date = date.strftime('%Y-%m-%d')
            plot_and_save_to_pdf(df, user_date, pdf)

if __name__ == "__main__":
    main()
