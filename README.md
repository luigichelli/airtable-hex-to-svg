
## Airtable Hex to SVG with Streamlit

### Introduction

This script, `hex_to_svg.py`, is designed to extract hex color values from an Airtable base, generate SVG images for each color, and then upload these SVGs to a specific attachment field in Airtable. The script also uses a public GitHub repository to host the SVG files. This allows you to visualize the hex colors directly within Airtable.

### Prerequisites

- Python 3.x
- Streamlit
- An Airtable account and a base with a table containing hex color values
- A GitHub account and a new public repository

### Installation

1. **Create a new public GitHub repository**: This repository will be used to host the SVG files. Make sure it is public so that the SVGs can be accessed by Airtable.

2. Download or clone this code repository to your local machine:

   ```bash
   git clone https://github.com/luigichelli/airtable-hex-to-svg.git
   ```

3. Navigate to the project directory:

   ```bash
   cd airtable-hex-to-svg
   ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

To run this script, you need to set up a `.env` file in the root directory of the project. This `.env` file should contain the following environment variables:

```plaintext
API_KEY=your_airtable_api_key
BASE_URL=your_airtable_base_url
TABLE_NAME=your_airtable_table_name
HEX_FIELD=your_hex_field_name
SVG_FIELD=your_svg_field_name
GITHUB_REPO_URL=your_new_public_github_repo_url
GITHUB_RAW_URL=your_new_public_github_raw_url
```

Replace the values with your own information.

- `API_KEY`: Your Airtable API key
- `BASE_URL`: The URL of your Airtable base
- `TABLE_NAME`: The name of the table in your Airtable base that contains the hex values
- `HEX_FIELD`: The field name where the hex values are stored
- `SVG_FIELD`: The attachment field where the SVGs will be uploaded
- `GITHUB_REPO_URL`: The URL of your new public GitHub repository, such as https://github.com/yourgithubusername/airtable-hex-to-svg.git
- `GITHUB_RAW_URL`: The raw URL where the SVGs are hosted in your new public GitHub repository, such as https://raw.githubusercontent.com/yourgithubusername/airtable-hex-to-svg/main/SVGs/

### Usage

After setting up your `.env` file, you can run the script with:

```bash
streamlit run hex_to_svg.py
```

This will start the extraction, SVG creation, and upload process.
