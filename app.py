from flask import Flask, request, render_template
import requests
from .prompter import create_prompt

app = Flask(__name__)

@app.route('/prompt', methods=['POST'])
def prompt():
    sku_id = input("Enter the sku id to generate video prompt: ")
    url = f'https://mooninternalapi.1mg.com/search/__onemg-internal__/v1/skus/{sku_id}/by_id'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "locale": "en",
        "location": "Gurgaon",
        "fields_hash": {
            "sku_fields": [
                "description_tags",
                "image_urls",
                "cropped_image_urls",
                "attributes_original",
                "attributes_nested",
                "locations",
                "sku_search_attributes",
                "tax_definition",
                "product_form_info",
                "other_composition",
                "udp_data",
                "transformed_image_urls",
                "transformed_cropped_image_urls",
                "ratings",
                "onemg_cash_usage",
                "average_rating",
                "total_ratings",
                "page_references",
                "authors",
                "social_cue_data",
                "supporting_fields",
                "info_for_honcode",
                "manufacturer",
                "business_category",
                "sku_attributes",
                "product_tags",
            ],
            "exclude": True
        },

        "filters": None,
        "country": None,
        "is_freebie": False,
        "source_fields": "sd",
        "search_in_freebie": True
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        json_data = response.json().get('data')
    else:
        return "Error:", response.status_code

    result = create_prompt(json_data)
    return render_template('index.html', result=result)
