import funcs

list_id = 246
url = f"https://api.hubapi.com/contacts/v1/lists/{list_id}/contacts/all?property=hs_linkedin_url"
api_key, headers, url = hs_prepare_request(url, "../config/hs_key.txt")

# Fetch all contacts from the HubSpot list
all_contacts = hs_fetch_list_contacts(api_key, headers, url, list_id)
print(f"Total Contacts Retrieved: {len(all_contacts)}")

print(all_contacts)
