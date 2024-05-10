import pandas as pd
import os
import re
from datetime import datetime
from constants import (
    RETAILER_PRICING_CSV, PINCODE_CSV, BESTSELLER_CSV,
    SEARCH_CSV, FEALTIME_RETAILER_PRICING_CSV, REALTIME_PINCODE_CSV,
    MAPPING_CSV, RAW_PINCODE_CSV, RAW_REALTIME_PINCODE_CSV
)
from constants import (
    PRODUCT_COLUMN, CATEGORY_COLUMN, WEBSITE_COLUMN, REVIEW_DATE_COLUMN,
    DELIVERY_DATE_COLUMN, SUBCATEGORY_COLUMN, ASIN_FSIN_COLUMN,
    URL_COLUMN
)
from constants import DATE_PICKER_FEATURE, TIME_PICKER_FEATURE

def days_difference(df):
    df = df.fillna("No Data")
    df = df.sort_values(by=list(df.columns.values)[-1])
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, ~df.columns.duplicated()]
    df.fillna('N/A', inplace=True)
    df.reset_index(drop=True, inplace=True)
    date_format = '%d-%m-%Y'
    for column in df.columns:
        if column.startswith(DELIVERY_DATE_COLUMN):
            column_date = column[14:24]
            day, month, year = column_date.split('-')
            formated_date = f"{year}-{month}-{day}"
            for i in range(len(df)):
                date_str = str(df.at[i, column])
                if date_str.strip().lower() == 'currently unavailable':
                    df.at[i, column] = 'Currently Unavailable'
                else:
                    try:
                        delivery_date = datetime.strptime(
                            date_str, date_format)
                        diff = delivery_date - \
                            datetime.strptime(formated_date, date_format)
                        if diff.days < 0 or diff.days > 25 and not diff.days == '':
                            df.at[i, column] = f'Error'
                        else:
                            df.at[i, column] = f'{diff.days} days'
                    except ValueError:
                        df.at[i, column] = ''
    return df

customize_view = {
    "Orient2": {
        "pincode": [DATE_PICKER_FEATURE],
        "realtime_pincode": [DATE_PICKER_FEATURE, TIME_PICKER_FEATURE],
        "realtime_pincode_dump": [DATE_PICKER_FEATURE, TIME_PICKER_FEATURE],
        "realtime_pricing_dump": [DATE_PICKER_FEATURE, TIME_PICKER_FEATURE],
        "pricing": [DATE_PICKER_FEATURE],
        'realtime_pricing': [DATE_PICKER_FEATURE, TIME_PICKER_FEATURE],
        'pincode_stock_availability': [DATE_PICKER_FEATURE],
        'mop': [],
        'drr_summary': [DATE_PICKER_FEATURE],
    },
    "Demo": {
        "pincode": [DATE_PICKER_FEATURE],
        "realtime_pincode": [DATE_PICKER_FEATURE, TIME_PICKER_FEATURE],
        "realtime_pincode_dump": [DATE_PICKER_FEATURE, TIME_PICKER_FEATURE],
        "realtime_pricing_dump": [DATE_PICKER_FEATURE, TIME_PICKER_FEATURE],
        "pricing": [DATE_PICKER_FEATURE],
        'realtime_pricing': [DATE_PICKER_FEATURE, TIME_PICKER_FEATURE],
        'pincode_stock_availability': [DATE_PICKER_FEATURE],
        "bestseller": [DATE_PICKER_FEATURE],
        "all_reviews": [],
        "search": [DATE_PICKER_FEATURE],
        'mop': [],
    },
    "Symphony": {
        "pricing": [DATE_PICKER_FEATURE],
        'mop': [],
    },
    "Atomberg": {
        "search": [DATE_PICKER_FEATURE],
        "pricing": [DATE_PICKER_FEATURE],
        "bestseller": [DATE_PICKER_FEATURE],
        "all_reviews": [],
        'mop': [],
    },
    "Kaff": {
        "pricing": [DATE_PICKER_FEATURE],
        "pincode": [DATE_PICKER_FEATURE],
        'pincode_stock_availability': [DATE_PICKER_FEATURE],
    }

}

class ViewDataHelper:
    """
    A helper class for managing multile table views.

    Args:
        view_name (str): The name of the view.
        start_date (str, optional): The start date for filtering data.
        end_date (str, optional): The end date for filtering data.
        start_time (str, optional): The start time for filtering data.
        end_time (str, optional): The end time for filtering data.
        Category (str, optional): The category for filtering data.
        Website (str, optional): The website for filtering data.
        product (str, optional): The product for filtering data.

    Attributes:
        start_date (str): The start date for filtering data.
        end_date (str): The end date for filtering data.
        start_time (str): The start time for filtering data.
        end_time (str): The end time for filtering data.
        Category (str): The category for filtering data.
        Website (str): The website for filtering data.
        product (str): The product for filtering data.
        view_name (str): The name of the view after normalization.
        company (str): The current user's company name.
        pricing_file_path (str): The path to the retailer pricing CSV file.
        pincode_file_path (str): The path to the pincode CSV file.
        bestseller_file_path (str): The path to the bestseller CSV file.
        client_folder_path (str): The path to the client folder.
        search_file_path (str): The path to the search CSV file.
        realtime_pricing_file_path (str): The path to the realtime retailer pricing CSV file.
        realtime_pincode_file_path (str): The path to the realtime pincode CSV file.
        mapping_file_path (str): The path to the mapping CSV file.
    """
    def __init__(self, view_name):
        if view_name in ['pincode_stock_availability', 'pincode']:
            self.view_name = 'pincode'
        elif view_name in ['drr_summary', 'realtime_pincode']:
            self.view_name = 'realtime_pincode'
        else:
            self.view_name = view_name

        self.pricing_file_path = os.path.join(RETAILER_PRICING_CSV)
        self.pincode_file_path = os.path.join(PINCODE_CSV)
        self.bestseller_file_path = os.path.join(BESTSELLER_CSV)
        # self.client_folder_path = os.path.join(CLIENT_DIR, self.company)
        self.search_file_path = os.path.join(SEARCH_CSV)
        self.realtime_pricing_file_path = os.path.join(FEALTIME_RETAILER_PRICING_CSV)
        self.realtime_pincode_file_path = os.path.join(REALTIME_PINCODE_CSV)
        self.mapping_file_path = os.path.join(MAPPING_CSV)
        self.raw_realtime_pincode_file_path = os.path.join(RAW_PINCODE_CSV)
        self.raw_pincode_file_path = os.path.join(RAW_REALTIME_PINCODE_CSV)

    def merge_with_mapping(self, data):
        """
        Merge the input data with mapping data based on specified columns.

        Args:
            data (pandas.DataFrame): The DataFrame to merge with mapping data.

        Returns:
            pandas.DataFrame: The merged DataFrame.
        """
        mapping_data = pd.read_csv(self.mapping_file_path)
        # Rename columns in the input data
        data.rename(columns={'Product': PRODUCT_COLUMN,
                             'product_name': PRODUCT_COLUMN}, inplace=True)
        # Define the columns to merge from the mapping data
        merge_columns = [PRODUCT_COLUMN]
        if CATEGORY_COLUMN in mapping_data.columns:
            merge_columns.append(CATEGORY_COLUMN)
        if WEBSITE_COLUMN in mapping_data.columns and 'website' not in data.columns:
            merge_columns.append(WEBSITE_COLUMN)
        if SUBCATEGORY_COLUMN in mapping_data.columns:
            merge_columns.append(SUBCATEGORY_COLUMN)
        # Remove this code once if the issue fixed in csv file
        if self.view_name == 'pricing':
            merge_columns.append("URL")
        # end
        # Merge the data
        merged_data = pd.merge(
            mapping_data[merge_columns], data, on=PRODUCT_COLUMN, how='inner')
        # Rename the 'website' column in the merged data
        merged_data.rename(columns={'website': WEBSITE_COLUMN}, inplace=True)

        return merged_data

    def process_pricing_data(self, data):
        """
        Process pricing data by cleaning and transforming the DataFrame.

        Args:
            data (pandas.DataFrame): The pricing data DataFrame to process.

        Returns:
            pandas.DataFrame: The processed pricing data DataFrame.
        """
        col_names_set = set()
        data = data[data["retailer"] != "No Retailer Found"]
        for col in data.columns:
            if col.startswith("price"):
                col_name = col.split("(")[1].split(":")[0]
                if col_name in col_names_set:
                    data = data.drop(col, axis=1)
                else:
                    col_names_set.add(col_name)
        data = self.merge_with_mapping(data)
        data.columns = [col[:-6] + '00)' if col.startswith(
            "price") and len(col) > 18 else col for col in data.columns]
        data.rename(columns={'product_name': 'Product', 'product_id': ASIN_FSIN_COLUMN,
                    'website': WEBSITE_COLUMN, 'retailer': 'Retailer', 'mop': 'MOP'}, inplace=True)
        data = data.drop("main_price_flag",
                         axis=1) if "main_price_flag" in data.columns else data
        data = data.drop(
            "product_id", axis=1) if "product_id" in data.columns else data
        data = data.drop(
            "product_index", axis=1) if "product_index" in data.columns else data
        data = data.dropna(axis=1, how='all')
        data["Product_name"] = data["Product_name"].str.split("_").str[1].str.replace('-Amazon', '').str.replace('-Flipkart', '')
        
        return data

    def pricing(self):
        """
        Load and process pricing data from a CSV file.

        Returns:
            pandas.DataFrame: The processed pricing data DataFrame.
        """
        df = pd.read_csv(self.pricing_file_path)
        df = self.process_pricing_data(df)
        # Remove this code once if the issue fixed in csv file
        df = df.drop(ASIN_FSIN_COLUMN,
                         axis=1) if ASIN_FSIN_COLUMN in df.columns else df
        df['ASIN/FSIN'] = df['URL'].str.split('/').str[-1]
        df = df.drop('URL', axis=1)
        df.insert(0, 'ASIN/FSIN', df.pop('ASIN/FSIN'))
        # end
        return df

    def realtime_pricing(self):
        """
        Load and process real-time pricing data from a CSV file.

        Returns:
            pandas.DataFrame: The processed real-time pricing data DataFrame.
        """
        df = pd.read_csv(self.realtime_pricing_file_path)
        df = self.process_pricing_data(df)
        return df

    def process_pincode_file(self, file_name):
        df = pd.read_csv(file_name)
        df.rename(columns={'Product': PRODUCT_COLUMN,
                  'product_name': PRODUCT_COLUMN}, inplace=True)
        df = self.merge_with_mapping(df)
        df = df[df["RetailerName"] != "No Retailer Found"]
        df["Product_name"] = df["Product_name"].str.split("_").str[1].str.replace('-Amazon', '').str.replace('-Flipkart', '')
        return df
    
    def pincode(self):
        """
        Load, merge with mapping, and process pincode data from a CSV file.

        Returns:
            pandas.DataFrame: The processed pincode data DataFrame.
        """
        df = self.process_pincode_file(self.pincode_file_path)
        try:
            df = days_difference(df)
            error_value = any(df[col].str.contains('Error').any() for col in df.columns[1:] if col.startswith("delivery_date"))
            df = self.process_pincode_file(self.raw_pincode_file_path) if error_value else df
        except:
            # app.logger.error("An exception occurred", exc_info=True)
            df = self.process_pincode_file(self.raw_pincode_file_path)
        return df

    def realtime_pincode(self):
        """
        Load and process real-time pincode data from a CSV file.

        Returns:
            pandas.DataFrame: The processed real-time pincode data DataFrame.
        """
        df = self.process_pincode_file(self.realtime_pincode_file_path)
        try:
            df = days_difference(df)
            error_value = any(df[col].str.contains('Error').any() for col in df.columns[1:] if col.startswith("delivery_date"))
            df = self.process_pincode_file(self.raw_realtime_pincode_file_path) if error_value else df
        except:
            # app.logger.error("An exception occurred", exc_info=True)
            df = self.process_pincode_file(self.raw_realtime_pincode_file_path)
        df.columns = [
            col[:-6] + '00)' if DELIVERY_DATE_COLUMN in col else col for col in df.columns]
        return df

    def search(self):
        """
        Load and process search data from a CSV file.

        Returns:
            pandas.DataFrame: The processed search data DataFrame.
        """
        df = pd.read_csv(self.search_file_path)
        df = df.drop(['amazon-prime_flipkart-assured', 'mrp'],
                     axis=1, errors='ignore')
        df.columns = df.columns.str.replace('search_', '')
        df.rename(columns={'category': CATEGORY_COLUMN, 'product_url': URL_COLUMN, 'website': 'Site', 'product_name': 'Product', 'is_sponsored': 'Sponsored', 'discount_price': 'Price',
                           'product_rating': 'Rating', 'number_of_ratings': 'Total Ratings'}, inplace=True)
        df["Sponsored"].replace(
            {0: 'Organic', 1: 'Ads', 2: 'AdsH', 3: 'Banner'}, inplace=True)
        return df

    def bestseller(self):
        """
        Load and process search data from a CSV file.

        Returns:
            pandas.DataFrame: The processed search data DataFrame.
        """
        df = pd.read_csv(self.bestseller_file_path)
        date_objects = [datetime.strptime(re.search(
            r'\d{4}-\d{2}-\d{2}', col).group(), '%Y-%m-%d') for col in df.columns[7:]]
        three_months_ago = max(date_objects) - pd.DateOffset(months=3)
        filtered_columns = [col for col, date_obj in zip(
            df.columns[7:], date_objects) if three_months_ago <= date_obj <= max(date_objects)]
        df = df.loc[~(df.filter(like='bestseller').eq(1000).all(axis=1))]
        df = df[['category', 'product_id', 'product_name', 'crawling_time',
                 'rating', 'reviews', 'price'] + filtered_columns]
        df.columns = df.columns.str.replace('bestseller_', '')
        df.rename(columns={'category': CATEGORY_COLUMN, 'product_id': 'ASIN/FSN', 'product_name': 'Product',
                           'crawling_time': 'Time', 'rating': 'Rating', 'reviews': 'Reviews', 'price': 'Price/Range'}, inplace=True)
        # df.insert(loc=2, column='Product_URL',
        #           value='https://www.amazon.in/dp/' + df['ASIN/FSN'].astype(str))
        df['Time'] = df['Time'].str.replace(
            r'[\[\]-]', '', regex=True).replace({'5': '6', '1': '10'})
        return df

    # def all_reviews(self):
    #     """
    #     Load and process all reviews data from the client folder path.

    #     Returns:
    #         pandas.DataFrame: The processed all reviews data DataFrame.
    #     """
    #     df = pd.read_csv(load_data_from_dir(
    #         self.client_folder_path)).fillna('N/A')
    #     df = df.drop(['Number_of_comments', 'Review_Views',
    #                  'Review_helpful'], axis=1)
    #     date_list = df[REVIEW_DATE_COLUMN].to_list()
    #     date_list.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
    #     df[REVIEW_DATE_COLUMN] = pd.to_datetime(df[REVIEW_DATE_COLUMN])
    #     df[REVIEW_DATE_COLUMN] = df[REVIEW_DATE_COLUMN].dt.strftime('%Y-%m-%d')
    #     return df

    # def mop(self):
    #     df1 = pd.read_csv(os.path.join(
    #         CSV_DIR, current_user.company, "MOP.csv"))
    #     df2 = pd.read_csv(os.path.join(
    #         CSV_DIR, current_user.company, "Retailer_Pricing.csv"))
    #     df2 = pd.concat(
    #         [df2[['product_name', 'retailer']], df2.iloc[:, -1]], axis=1)
    #     df = df1.merge(df2, left_on="Product_Name",
    #                    right_on="product_name", how="inner")
    #     df.insert(0, 'Product_name', df['Product_Name'])
    #     df = df.drop(["product_name", "Product_Name"], axis=1)
    #     df = df[df[list(df.columns.values)[-1]] > 0]
    #     df = self.merge_with_mapping(df)
    #     df["Product_name"] = df["Product_name"].str.split("_").str[1].str.replace('-Amazon', '').str.replace('-Flipkart', '')
    #     return df

    def get_data(self):
        """
        Get data based on the view name, filter rows and columns, and get the datetime range.
        This is the heart of this class.

        Returns:
            pandas.DataFrame: The processed data DataFrame.
            tuple: A tuple containing the range of dates and times.
        """
        view_function = getattr(self, self.view_name)
        df = view_function()
        df = df.dropna(axis=1, how='all')
        return df
