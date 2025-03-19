import hs_funcs
import yaml
import pandas as pd

# Get API Key
with open("../config/config.yaml", "r") as f:
    config = yaml.safe_load(f)
api_key = config["hubspot_api_key"]

# Load outreach results
outreach_results = pd.read_csv("../data/linkedin_outreach_results.csv")

# Update contacts in HubSpot
properties_to_update = ["organic_social_outreached", "outreach_note"]
hs_funcs.HS.hs_update_contacts(api_key, outreach_results, properties_to_update)

# Confirmation
print("\nHubSpot contacts updated with outreach decisions and notes.")
