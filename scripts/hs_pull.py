import hs_funcs
import yaml

# Get key
with open("../config/config.yaml", "r") as f:
    config = yaml.safe_load(f)
api_key = config["hubspot_api_key"]

# Prepare HS info
list_id = 246
url = f"https://api.hubapi.com/contacts/v1/lists/{list_id}/contacts/all?property=hs_linkedin_url&property=firstname&property=lastname&property=organic_social_outreached&property=post_name"
api_key, headers, url = hs_funcs.HS.hs_prepare_request(url, api_key)

# Fetch all contacts from the HubSpot list
response = hs_funcs.HS.hs_fetch_list_contacts(api_key, headers, url, list_id)

# Parse all hubspot contacts
print("\nParsing contacts from Hubspot...\n")
properties = ["firstname", "lastname", "hs_linkedin_url", "organic_social_outreached", "post_name"]
contacts = hs_funcs.HS.parse_hubspot_contacts(response, properties)
unreached_contacts = contacts[(contacts["organic_social_outreached"] != "Yes") & (contacts["organic_social_outreached"] != "No")]
print(f"\Contacts not yet outreached to:\n{unreached_contacts}")

# Save contacts to data/non_outreached.csv
unreached_contacts.to_csv("../data/non_outreached.csv")

# Status Update
print("\nSaved contacts to /data/non_outreached.csv")
