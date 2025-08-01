from cloudant.client import Cloudant

# Replace with your actual values
API_KEY = "u8WxfPdj09VCy01Fbb8ga4_ugdwN2rq6IVTObCnuoVLX"
ACCOUNT_NAME = "551fce69-b35d-4a14-b219-a7bd6c0e30d3-bluemix"  # Just the prefix before `.cloudantnosqldb.appdomain.cloud`
DB_NAME = "tasks"

# Create the client using IAM authentication
client = Cloudant.iam(account_name=ACCOUNT_NAME, api_key=API_KEY, connect=True)

# Access your database
db = client[DB_NAME]
