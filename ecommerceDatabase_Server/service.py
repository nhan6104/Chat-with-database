import pandas as pd
import os
import sys
import json
import numpy as np
import numpy as np
# conn = sqlite3.connect("sales.db")
# cur = conn.cursor() 

class toolAnalysis:
    def __init__(self, dataframe):
        self.df = dataframe

    def get_unique_values(self, column_name):
        uniques = self.df[column_name].unique()
        message = f"There are {len(uniques)} unique value in {column_name} column."
        payload = {
            'type': 'text',
            'data': {
                "message": message,
                "list_unique_values": list(uniques)
            }
        }
        return payload
    
    def get_empty_values(self, column_name):
        numEmptyValue = self.df[column_name].isna().sum()
        message = f"There are {numEmptyValue} empty values"
        payload = {
            'type': 'text',
            'data': message
        }
        return payload
    
    def get_nonempty_values(self, column_name):
        numNonEmptyValue = len(self.df[column_name]) - self.df[column_name].isna().sum()
        message = f"There are {numNonEmptyValue} nonempty values"
        payload = {
            'type': 'text',
            'data': message
        }
        return payload
    # int64, float64
    def get_max_values(self, column_name):
        maxValue = self.df[column_name].max()
        message = f"The max value is {maxValue}"
        payload = {
            'type': 'text',
            'data': message
        }
        return payload
    
    def get_min_value(self, column_name):
        minValue = self.df[column_name].min()
        message = f"The min value is {minValue}"
        payload = {
            'type': 'text',
            'data': message
        }
        return payload
    
    def get_median_value(self, column_name):
        medianValue = self.df[column_name].median()
        message = f"The median value is {medianValue}"
        payload = {
            'type': 'text',
            'data': message
        }
        return payload
    
    def get_mean_values(self, column_name):
        meanValue = self.df[column_name].mean()
        message = f"The mean value is {meanValue}"
        payload = {
            'type': 'text',
            'data': message
        }
        return payload
    
    def get_mode_values(self, column_name):
        modeValue = self.df[column_name].mode()
        message = f"The mode value is {modeValue}"
        payload = {
            'type': 'text',
            'data': message
        }
        return payload
    
    def get_histogram(self, column_name):
        counts, bin_edges = np.histogram(self.df[column_name], bins='auto')

        hist_data = {
            "bin_edges": bin_edges.tolist(),
            "counts": counts.tolist()
        }
        payload = {
            'type': 'histogram_chart',
            'data': hist_data
        }
        return payload
    
    def get_correlation(self):
        lst_columns_choose = []
        for col in list(self.df.columns.sort_values(ascending=False)):
            
            unique_value_percent = (len(self.df[col].unique()) / len(self.df[col]) < 0.95) and (not col.endswith('id')) # loại bỏ các biến như id, hoặc có số lượng các giá trị khác nhau nhiều
            qualitive_value = set((0,1)) != set(self.df[col].unique())
            if self.df[col].dtype in ['int64', 'float64'] and not self.df[col].isna().all() and self.df[col].var() != 0 and unique_value_percent and qualitive_value:
                lst_columns_choose += [col]

        # biến định lượng
        correlation_matrix = self.df[lst_columns_choose].corr(method='pearson')
        
        # loại bỏ dư thừa
        redundant_col = []
        for row in correlation_matrix.columns:
            if row in redundant_col:
                continue
            for col in correlation_matrix.columns:
                if row != col and abs(correlation_matrix.loc[row, col]) > 0.98:
                    redundant_col += [col]

        # print(redundant_col)
        correlation_matrix = correlation_matrix.drop(redundant_col, axis=1)
        correlation_matrix = correlation_matrix.drop(redundant_col, axis=0)
        print(type(correlation_matrix))
        payload = {
            'type': 'correlation_chart',
            'data': correlation_matrix.to_json(orient='records')
        }
        return payload


    def describeColumn(self):
        df = self.df
        template_describe = "Total_Data: {}\nColumn_name: {}\nData_type: {}\nUnique_value: {}\nEmpty_Value: {}\n"
        describe_list = []
        total_data, _ = df.shape
        
        for col in df.columns.to_list():
            unique_value = len(df[col].unique())
            empty_value = df[col].isna().sum()
            describe = None
            
            # Checking the data type and structure of the column
            col_dtype = str(df[col].dtype)
            first_value = str(df.loc[0, col])  # Check the first value for specific patterns
            
            if col_dtype == 'object' and first_value.startswith('['):
                typ = "list_type"
                describe = {
                    "Total_Data": total_data, 
                    "Column_name": col,
                    "Data_type": typ,
                    "Unique_value": unique_value,
                    "Empty_value": empty_value
                }
            
            elif col_dtype == 'object' and first_value.startswith('"'):
                typ = "string_type"
                describe = {
                    "Total_Data": total_data, 
                    "Column_name": col,
                    "Data_type": typ,
                    "Unique_value": unique_value,
                    "Empty_value": empty_value
                }
            
            else:
                describe = {
                    "Total_Data": total_data, 
                    "Column_name": col,
                    "Data_type": col_dtype,
                    "Unique_value": unique_value,
                    "Empty_value": empty_value
                }

            # Convert int64 values to int
            describe = {key: (int(value) if isinstance(value, np.int64) else value) for key, value in describe.items()}
            
            describe_list.append(describe)
        
        # Serialize describe_list to JSON
        payload = {
            'type': 'text',
            'data': describe_list  # Now it should work fine
        }
        return payload


# if __name__ == '__main__':
#     etl = ETL('product')
#     etl.loadDataToCSV('fashion_accessories_2025_04_16')
#     df = pd.read_csv('fashion_accessories_2025_04_16.csv')
#     describe = describeCol(df)
#     matrix = describe.correlationInfo()
#     # print(val)
  
#     sns.set_theme(style="dark")
#     plt.figure(figsize=(18, 16))

#     # print(matrix)
#     heatmap = sns.heatmap(matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={"label": "test tingg"})
#     heatmap.set_title("test")
#     plt.show()
#     # print(etl.describeColumn(df))
#     # etl.extract('./amazon.csv', 'sales')
