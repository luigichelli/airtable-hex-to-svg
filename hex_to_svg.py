import streamlit as st
import requests
import svgwrite
import subprocess
import time
import os
from urllib.parse import quote
from decouple import config

# Print the current working directory
print("Current working directory:", os.getcwd())

# Create a subfolder named "SVGs" if it doesn't exist
if not os.path.exists("SVGs"):
    os.makedirs("SVGs")

# Your GitHub repository where SVG files will be stored
GITHUB_REPO_URL = config("GITHUB_REPO_URL")
GITHUB_RAW_URL = config("GITHUB_RAW_URL")

# Your Airtable settings with Base ID
API_URL_BASE = config("BASE_URL")
API_KEY = config("API_KEY")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
}

# Streamlit App
st.title("Airtable SVG Updater")

# User Input for table name
table_name = config("TABLE_NAME")

# Fetch and display field names based on selected table
hex_field = config("HEX_FIELD")
svg_field = config("SVG_FIELD")

# Execute when the 'Run' button is clicked
if st.button("Run"):
    
    # Fetch records from Airtable with rate-limit handling
    try:
        response = requests.get(f"{API_URL_BASE}/{table_name}", headers=HEADERS)
        response.raise_for_status()
        time.sleep(0.3)  # Introduce a 200ms delay to handle rate limits
    except requests.RequestException as e:
        st.error(f"Failed to fetch records: {e}")
        st.stop()

    records = response.json().get("records", [])

    if not records:
        st.warning("No records found.")
        st.stop()

    # Step 1: Generate SVGs
    for record in records:
        record_id = record["id"]
        fields = record.get("fields", {})
        hex_value = fields.get(hex_field, None)
        
        if not hex_value or not hex_value.startswith("#"):
            st.write(f"[Warning] Skipping record {record_id} due to missing or invalid HEX value.")
            continue
        
        # Create a new SVG with a simplified structure
        svg_content = f'''
        <svg width="64" height="64" xmlns="http://www.w3.org/2000/svg">
            <rect width="64" height="64" fill="{hex_value}" />
        </svg>
        '''
        
        # Save the SVG content to a file
        svg_path = f"SVGs/{hex_value}.svg"
        with open(svg_path, "w") as svg_file:
            svg_file.write(svg_content)
    
    # Step 2: Commit and push all SVGs to GitHub
    commit_status = subprocess.run(["git", "status", "--porcelain"], stdout=subprocess.PIPE)
    if commit_status.stdout:
        # There are changes to commit
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Add SVGs"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
        except subprocess.CalledProcessError as e:
            st.error(f"Failed to update GitHub: {e}")
            st.stop()
    else:
        # There are no changes to commit
        st.info("No changes to commit.")

    # Wait for some time or ask for user confirmation
    st.info("Waiting for GitHub to process the new files. This could take a few seconds.")
    time.sleep(5)  # Adjust as needed.

    # Step 3: Update Airtable
    updated_count = 0
    for record in records:
        record_id = record["id"]
        fields = record.get("fields", {})
        hex_value = fields.get(hex_field, None)
        
        if not hex_value or not hex_value.startswith("#"):
            continue
        
        encoded_hex_value = quote(hex_value, safe='') # Encode the '#' character
        svg_url = f"{GITHUB_RAW_URL}/{encoded_hex_value}.svg"
        st.write(svg_url)
        
        try:
            data = {
                "fields": {
                    svg_field: [
                        {"url": svg_url, "filename": f"{hex_value}.svg"}
                    ]
                }
            }
            response = requests.patch(f"{API_URL_BASE}/{table_name}/{record_id}", headers=HEADERS, json=data)
            response.raise_for_status()
            time.sleep(0.2)
        except requests.RequestException as e:
            st.error(f"Failed to update record {record_id}: {e}")
            continue
        
        st.success(f"Successfully updated record {record_id} with SVG.")
        updated_count += 1

    st.info(f"Successfully updated {updated_count} records with SVGs.")
