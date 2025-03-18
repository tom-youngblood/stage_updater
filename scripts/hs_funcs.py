import requests
import pandas as pd

class HS:
    def hs_prepare_request(url, api_key):
        # Headers for authentication
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        return api_key, headers, url

    def hs_fetch_list_contacts(api_key, headers, url, list_id):
        contacts = []
        params = {
            "count": 100  # HubSpot returns up to 100 contacts per request
        }

        while True:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                print(f"Error: {response.status_code}, {response.text}")
                break

            data = response.json()

            # Extract contacts and add to the list
            if "contacts" in data:
                contacts.extend(data["contacts"])

            # Check for pagination (if there are more contacts to fetch)
            if data.get("has-more", False) and "vid-offset" in data:
                params["vidOffset"] = data["vid-offset"]  # Update pagination parameter
            else:
                break  # No more contacts to fetch

        return contacts

    def parse_hubspot_contacts(response):
        """
        Extracts vid and all properties from a list of HubSpot contacts (v1 API).
        """
        contacts_list = []

        all_properties = [
            "firstname",
            "lastname",
            "email",
            "company",
            "createdate",
            "organic_social_stage",
            "organic_social_outreached",
            "linkedin_profile_url_organic_social_pipeline",
            "latest_funding_date",
            "latest_funding_stage",
            "total_funding",
            "post_id",
            "post"
        ]

        for contact in response:
            parsed_data = {"vid": contact.get("vid")}  # Extract vid

            # Extract all requested properties, setting None if missing
            if "properties" in contact:
                for prop in all_properties:
                    if prop in contact["properties"]:
                        parsed_data[prop] = contact["properties"][prop].get("value")
                    else:
                        parsed_data[prop] = None  # Ensures consistency across all rows

            contacts_list.append(parsed_data)  # Add to list

        return pd.DataFrame(contacts_list)
