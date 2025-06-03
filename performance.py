import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sorting import insertion_sort, merge_sort

class PerformanceAnalyzer:
    def __init__(self):
        self.results = {
            "algorithm": [],
            "data_size": [],
            "execution_time": [],
            "has_secondary_sort": []
        }
    
    def analyze_algorithm(self, algorithm, items, primary_key, secondary_keys=None, name=None):
        """
        Analyze performance of a sorting algorithm
        
        Args:
            algorithm: sorting function to analyze
            items: data to sort
            primary_key: attribute for primary sorting
            secondary_keys: list of tuples for secondary sorting
            name: name of the algorithm (optional)
        """
        # Make a copy to avoid modifying the original list
        items_copy = items.copy()
        
        # Run the algorithm and measure time
        start_time = time.time()
        algorithm(items_copy, primary_key, secondary_keys)
        execution_time = time.time() - start_time
        
        # Store results
        algo_name = name if name else algorithm.__name__
        self.results["algorithm"].append(algo_name)
        self.results["data_size"].append(len(items))
        self.results["execution_time"].append(execution_time)
        self.results["has_secondary_sort"].append(secondary_keys is not None)
        
        return execution_time
    
    def compare_algorithms(self, algorithms, data_sizes, generate_data_func, primary_key, secondary_keys=None):
        """
        Compare multiple algorithms with varying data sizes
        
        Args:
            algorithms: dictionary of {name: function} for algorithms
            data_sizes: list of different data sizes to test
            generate_data_func: function to generate test data of given size
            primary_key: attribute for primary sorting
            secondary_keys: list of tuples for secondary sorting
        """
        for size in data_sizes:
            # Generate data for this size
            data = generate_data_func(size)
            
            # Test each algorithm
            for name, func in algorithms.items():
                # Without secondary sorting
                self.analyze_algorithm(func, data, primary_key, None, f"{name} (Primary Only)")
                
                # With secondary sorting
                if secondary_keys:
                    self.analyze_algorithm(func, data, primary_key, secondary_keys, f"{name} (With Secondary)")
    
    def visualize_results(self):
        """Create visualizations of the performance data"""
        if not self.results["algorithm"]:
            print("No performance data to visualize")
            return
        
        # Convert results to DataFrame
        results_df = pd.DataFrame(self.results)
        
        # Group by algorithm and data size
        grouped = results_df.groupby(["algorithm", "data_size", "has_secondary_sort"])["execution_time"].mean().reset_index()
        
        # Plot execution time vs data size for each algorithm
        plt.figure(figsize=(10, 6))
        
        for algo in grouped["algorithm"].unique():
            algo_data = grouped[grouped["algorithm"] == algo]
            
            # For primary sort only
            primary_data = algo_data[algo_data["has_secondary_sort"] == False]
            if not primary_data.empty:
                plt.plot(primary_data["data_size"], primary_data["execution_time"], 
                         marker='o', linestyle='-', label=f"{algo}")
        
            # For secondary sort
            secondary_data = algo_data[algo_data["has_secondary_sort"] == True]
            if not secondary_data.empty:
                plt.plot(secondary_data["data_size"], secondary_data["execution_time"], 
                         marker='s', linestyle='--', label=f"{algo} (with secondary)")
        
        plt.title("Sorting Algorithm Performance Comparison")
        plt.xlabel("Data Size")
        plt.ylabel("Execution Time (seconds)")
        plt.legend()
        plt.grid(True)
        
        # Save the plot
        plt.savefig("sorting_performance.png")
        plt.close()
        
        return "sorting_performance.png"

    def get_results_dataframe(self):
        """Return performance results as a pandas DataFrame"""
        return pd.DataFrame(self.results)
    
    def get_time_complexity_analysis(self):
        """Generate time complexity analysis report"""
        complexity = {
            "Insertion Sort (Loop-based)": "O(n²) - Quadratic time complexity",
            "Insertion Sort (Loop-based) (With Secondary)": "O(n²) - With additional constant factor for logical operations",
            "Merge Sort (Recursive)": "O(n log n) - Linearithmic time complexity",
            "Merge Sort (Recursive) (With Secondary)": "O(n log n) - With additional constant factor for logical operations"
        }
        
        return complexity
