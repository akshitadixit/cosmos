import openai
import requests
import dotenv
import os

dotenv.load_dotenv()
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def create_prompt(json_object):
    BASE_PROMPT = """
                    You are an assistant that takes json object and returns a prompt to create a video.
                    The json object is  containing sku or medicine data which will contain a description of the medicine and its uses, side effects, and other relevant information from the json object.
                    The assistant will return a response which summarizes the information in the json object and turn it to a prompt to generate a realistic video about the medicine.
                    The response should contain a description of the video that should be generated.
                    The response should be a maximum of 2000 tokens long.
                    The response should be written in a way that another AI can generate a realistic video about the medicine with the response.
                    The video should be realistic.
                    The video should be high quality.
                    The video should be strictly less than 20 seconds.
                    The video should be engaging and informative.
                    The video should be able to be used for marketing purposes.
                    The video should be able to be used for educational purposes.
                    The video should be able to be used for entertainment purposes.
                    The video should be able to be used for commercial purposes.
                    The video should be able to be used for any other purposes.

                    Below is a json object that contains information about a medicine. Only return the prompt I should use to generate a video about the medicine.

                    The primary message or goal of the video is we are aiming to educate and provide information.
                    Target Audience: This will help determine the level of detail and technical language we should use in the script. this video is for patients and healthcare professionals.
                    The video be straightforward and informative and reassuring?
                    Keep the length of the video as 20 seconds, which is suitable for social media platforms.
                    draft an informative script for a 20-second video about the medicine in the json object, including advice, warnings, and lifestyle tips.
                    select a female text-to-speech voiceover without any AI avatar.
                    length of video should be 20 seconds, video should be pure infromative, and please add advice or warnings and lifestyle tips as well. We don't want any AI avatar.
                    Keep it more professional.
                    The video duration should be below 30 seconds and the noise of music should be minimized
                    Make it more professional. Improve the font and the alignment.
                    {}

                    The script should strike a balance between being informative and engaging, catering to various purposes such as marketing, education, and entertainment. To maintain professionalism, opt for a female text-to-speech voiceover without any AI avatar.

                    Your primary objective is to deliver valuable insights and advice while adhering to a strict 20-second duration, ideal for social media platforms. Enhance the video's visual appeal by improving font alignment and ensuring minimal background music, minimizing distractions for the audience.

                    Audience: Patients and healthcare professionals.
                    Video Duration: 20 seconds or less.
                    Tone: Professional and informative.
                    Purpose: Educational, marketing, and entertainment.

                    Keep it less than 20 seconds.
                """
    # create a prompt
    prompt = BASE_PROMPT.format(json_object)
    # get the prompt from openai
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
    max_tokens=250,
    )
    response = chat_completion.choices[0].message.content
    # return the response
    return response

if __name__ == "__main__":
    # take sku id as input
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
        print("Error:", response.status_code)

    print(create_prompt(json_data))