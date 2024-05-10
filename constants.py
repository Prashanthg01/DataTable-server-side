import os

# column name constatnts
PRODUCT_COLUMN = 'Product_name'
CATEGORY_COLUMN = 'Category'
WEBSITE_COLUMN = 'Website'
REVIEW_DATE_COLUMN = 'Review_Date'
DELIVERY_DATE_COLUMN = 'delivery_date'
SUBCATEGORY_COLUMN = 'SubCategory'
PRODUCT_URL_COLUMN = 'Product_Url'
REVIEW_ID_COLUMN = 'Review_ID'
ASIN_FSIN_COLUMN = "ASIN/FSIN"
REVIEW_STARS_COLUMN = 'Review_Stars'
REVIEW_TEXT_COLUMN = 'Review_Text'
REVIEW_TITLE_COLUMN = 'Review_Title'
REVIEWER_NAME_COLUMN = 'Reviewer_Name'
FILE_NAME_COLUMN = 'File_name'
URL_COLUMN = 'URL'
PRODUCT_ID_COLUMN = 'Product_ID'
REVIEW_VIEWS_COLUMN = "Review_Views"
REVIEWS_HELPFUL_COLUMN = "Review_helpful"
REVIEWS_VERIFIED_COLUMN = "Review_Verified"
NUM_OF_COMMENTS_COLUMN = "Number_of_comments"
NUM_RATINGS_COLUMN = "Number_rating"
REVIEWER_ADDRESS_COLUMN = 'Reviewer_Address'
REVIEWER_COUNTRY_COLUMN = 'Reviewer_Country'
TOTAL_REVIEWS_COUNT_COLUMN = 'Total_Reviews_Count'
TOTAL_RATINGS_COUNT_COLUMN = 'Total_Ratings_Count'

# Feature constatnts
DATE_PICKER_FEATURE = 'datepicker'
TIME_PICKER_FEATURE = 'timepicker'
CATEGORY__FEATUR = 'category'
WEBSITE_FEATURE = 'website'

# csv constatnts
RETAILER_PRICING_CSV = 'Retailer_Pricing.csv'
PINCODE_CSV = 'Pincode.csv'
BESTSELLER_CSV = 'Bestseller.csv'
SEARCH_CSV = 'Search.csv'
FEALTIME_RETAILER_PRICING_CSV = "RealTime_Retailer_Pricing.csv"
REALTIME_PINCODE_CSV = "RealTime_Pincode.csv"
MAPPING_CSV = 'mapping.csv'
ALL_FILES_CSV = "All_files.csv"
PRODUCT_INFO_CSV = 'PRODUCT_INFO_client.csv'
FEATURES_CSV = 'features.csv'
MOP_REALTIME_CSV = 'MOP_realtime'
NEW_RELEASES_CSV = 'New_releases.csv'
RAW_PINCODE_CSV = 'RealTime_Pincode_raw.csv'
RAW_REALTIME_PINCODE_CSV = 'Pincode_raw.csv'

# default constatnts
DEFAULT_CATEGORY = 'All_Category'
DEFAULT_WEBSITE = 'All Websites'

# paths
MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CLIENT_DIR = os.path.join(MAIN_DIR, 'client')
BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, 'input_files', 'CSVs')
WORDCLOUD_DIR = os.path.join(BASE_DIR, 'static', 'wordclouds')
MAP_DIR = os.path.join(BASE_DIR, 'templates', 'maps')
PRICING = os.path.join(BASE_DIR, 'Retailer_Pricing.csv')
BEST = os.path.join(BASE_DIR, 'Bestseller.csv')
SEARCH = os.path.join(BASE_DIR, 'Search.csv')
PRODUCT_INFO = os.path.join(
    BASE_DIR, 'admin', 'utils', 'PRODUCT_INFO_client.csv')
INDIAN_STATE_JSON = os.path.join(
    BASE_DIR, 'admin', 'utils', 'indian-state.json')
INDIAN_GEOCODED_CSV = os.path.join(
    BASE_DIR, 'admin', 'utils', 'geocoded_data.csv')
INDIAN_STATE_LIST = ["Andhra Pradesh", "Arunachal Pradesh ", "Assam", "Bihar", "Chhattisgarh",
                     "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand",
                     "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
                     "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
                     "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
                     "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli",
                     "Daman and Diu", "Lakshadweep", "Delhi", "Puducherry"]

ALLOWED_FILE_EXTENSIONS = ["CSV"]
