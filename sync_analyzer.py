import datetime
import re
import time

import matplotlib.pyplot as plt
import pandas as pd


class LogParser:
    def __init__(self, log_file_path):
        """
        Initialize the LogParser with the path to the log file.

        Args:
        - log_file_path (str): Path to the log file.
        """
        self.log_file_path = log_file_path
        self.log_data = self.read_log_file()

    def read_log_file(self):
        """
        Read the log file and return its content as a list of lines.

        Returns:
        - list: List of lines from the log file.
        """
        with open(self.log_file_path) as file:
            return file.readlines()

    def extract_timestamps_numbers(self):
        """
        Extract timestamps and numbers from the log data.

        Returns:
        - tuple: Two lists - timestamps and corresponding numbers.
        """
        timestamps = []
        timestamp_pattern = re.compile(r"INFO \[(.*?)\] Imported")
        numbers = []
        number_pattern = re.compile(r"segment\s+number=([\d,]+)")

        for line in self.log_data:
            timestamp_match = timestamp_pattern.findall(line)
            number_match = number_pattern.search(line)
            if timestamp_match and number_match:
                timestamp_str = timestamp_match[0]
                timestamp = datetime.datetime.strptime(
                    timestamp_str, "%m-%d|%H:%M:%S.%f"
                ).replace(year=2023)
                timestamps.append(timestamp)

                number_str = number_match.group(1)
                number = int(number_str.replace(",", ""))
                numbers.append(number)

        return timestamps, numbers


class SyncData:
    def __init__(self, timestamps, numbers):
        """
        Initialize SyncData with timestamps and corresponding numbers.

        Args:
        - timestamps (list): List of timestamps.
        - numbers (list): List of numbers.
        """
        self.timestamps = timestamps
        self.numbers = numbers


class SyncView:
    def __init__(self, sync_data: SyncData):
        """
        Initialize SyncView with SyncData.

        Args:
        - sync_data (SyncData): SyncData object containing timestamps and numbers.
        """
        self.sync_data = sync_data

    def plot_data(self):
        """
        Plot the data using matplotlib.
        """
        plt.plot(self.sync_data.timestamps, self.sync_data.numbers, marker="o")
        plt.xlabel("Time")
        plt.ylabel("Block Number")
        plt.title("Sync Speed")
        plt.xticks(rotation=45)
        plt.tight_layout()

    def save_plot(self, file_path):
        """
        Save the plot to the specified file path.

        Args:
        - file_path (str): Path to save the plot.
        """
        plt.savefig(file_path)


class SyncController:
    def __init__(self, log_file_path, plot_file_path, csv_file_path):
        """
        Initialize SyncController with paths and create LogParser, SyncData, and SyncView objects.

        Args:
        - log_file_path (str): Path to the log file.
        - plot_file_path (str): Path to save the plot.
        - csv_file_path (str): Path to save CSV data.
        """
        self.log_parser = LogParser(log_file_path)
        timestamps, numbers = self.log_parser.extract_timestamps_numbers()
        self.sync_data = SyncData(timestamps, numbers)
        self.sync_view = SyncView(self.sync_data)
        self.plot_file_path = plot_file_path
        self.csv_file_path = csv_file_path

    def generate_plot(self):
        """
        Generate and save the plot.
        """
        self.sync_view.plot_data()
        self.sync_view.save_plot(self.plot_file_path)

    def save_to_csv(self):
        """
        Save data to a CSV file.
        """
        data = {
            "timestamp": self.sync_data.timestamps,
            "numbers": self.sync_data.numbers,
        }
        df = pd.DataFrame(data)
        df.to_csv(self.csv_file_path, mode="w", index=False)


if __name__ == "__main__":
    # Set file paths
    log_file_path = "ethereum-node-sync.log"
    plot_file_path = "./output/sync_speed.png"
    csv_file_path = "./output/sync_speed.csv"

    # Measure execution time
    start_time = time.time()

    # Create and run the SyncController
    sync_controller = SyncController(log_file_path, plot_file_path, csv_file_path)
    sync_controller.generate_plot()
    sync_controller.save_to_csv()

    # Print execution time
    print(f"Execution time: {time.time() - start_time} seconds")
    print(f"Plots saved to: {plot_file_path}")
    print(f"CSV data saved to: {csv_file_path}")
