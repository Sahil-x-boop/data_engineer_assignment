import ast


data = "{'name': 'Bob', 'age': 30, 'city': 'New York'}"

# thats how we convert the string to a dictionary
try:
    site_info = ast.literal_eval(data)
    print("Converted data:", site_info)
    print("Type of site_info:", type(site_info))
except Exception as e:
    print("An error occurred:", e)
    site_info = {}