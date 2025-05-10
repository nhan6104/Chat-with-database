import pandas as pd

dataframe = pd.read_csv('product.csv', low_memory=False)

get_median_value = {
   "name": "get_median_value",
    "description": "Get median value in column with type item",
    "parameters": {
        "type": "object",
        "properties": {
            "column_name": {
                "type": "string",
                "enum": dataframe.columns.to_list(),
                "description": "Name of column to search",
            },
        },
        "required": ["column_name"],
    },
}


get_unique_values = {
   "name": "get_unique_values",
    "description": "Get unique value in column with type item",
    "parameters": {
        "type": "object",
        "properties": {
            "column_name": {
                "type": "string",
                "enum": dataframe.columns.to_list(),
                "description": "Name of column to search",
            }
        },
        "required": ["column_name"],
    },
}


get_empty_values = {
   "name": "get_empty_values",
    "description": "Get nunber of empty value in column with type item",
    "parameters": {
        "type": "object",
        "properties": {
            "column_name": {
                "type": "string",
                "enum": dataframe.columns.to_list(),
                "description": "Name of column to search",
            }
        },
        "required": ["column_name"],
    },
}


get_nonempty_values = {
   "name": "get_nonempty_values",
    "description": "Get number of nonempty value in column with type item",
    "parameters": {
        "type": "object",
        "properties": {
            "column_name": {
                "type": "string",
                "enum": dataframe.columns.to_list(),
                "description": "Name of column to search",
            },
        },
        "required": ["column_name"],
    },
}


get_max_values = {
   "name": "get_max_values",
    "description": "Get max value in column with type item",
    "parameters": {
        "type": "object",
        "properties": {
            "column_name": {
                "type": "string",
                "enum": dataframe.columns.to_list(),
                "description": "Name of column to search",
            }
        },
        "required": ["column_name"],
    },
}


get_min_value = {
   "name": "get_min_value",
    "description": "Get min value in column with type item",
    "parameters": {
        "type": "object",
        "properties": {
            "column_name": {
                "type": "string",
                "enum": dataframe.columns.to_list(),
                "description": "Name of column to search",
            },
        },
        "required": ["column_name"],
    },
}

get_mean_values = {
   "name": "get_mean_values",
    "description": "Get mean value in column with type item",
    "parameters": {
        "type": "object",
        "properties": {
            "column_name": {
                "type": "string",
                "enum": dataframe.columns.to_list(),
                "description": "Name of column to search",
            },
        },
        "required": ["column_name"],
    },
}


get_mode_values = {
   "name": "get_mean_values",
    "description": "Get mode value in column with type item",
    "parameters": {
        "type": "object",
        "properties": {
            "column_name": {
                "type": "string",
                "enum": dataframe.columns.to_list(),
                "description": "Name of column to search",
            },
        },
        "required": ["column_name"],
    },
}


# get_histogram = {
#    "name": "get_histogram",
#     "description": "Get histogram chart to view data in column with type item",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "column_name": {
#                 "type": "string",
#                 "enum": dataframe.columns.to_list(),
#                 "description": "Name of column to view chart",
#             },
#             "type_item": {
#                 "type": "string",
#                 "enum": dataframe['_visible_impression_info_amplitude_category_l1_name'].columns.to_list(),
#                 "description": "Type of item to search",
#             },
#         },
#         "required": ["column_name", "type_item"],
#     },
# }

# get_correlation = {
#    "name": "get_correlation",
#     "description": "Get correlation of data",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "column_names": {
#                 "type": "array",
#                 "items":{
#                             "type": "string", 
#                             "enum": dataframe.columns.to_list()
#                         },
#                 "description": "List of column to view correlation",
#             },
#             "type_item": {
#                 "type": "string",
#                 "enum": ["clothes_woman", "clothes_man"],
#                 "description": "Type of item to seah",
#             },
#         },
#         "required": ["column_names", "type_item"],
#     },
# }


get_correlation = {
   "name": "get_correlation",
    "description": "Get correlation of data"
}


describe_column = {
   "name": "describeColumn",
    "description": "Get general description of database",
}


