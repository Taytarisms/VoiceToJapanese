import traceback
from transformers import pipeline
import requests
import json

use_deepl = False
deepl_api_key = ''
fugu_translator = None

def initialize():
    global fugu_translator
    fugu_translator = pipeline(
        'translation', model='./models--staka--fugumt-en-ja/snapshots/2d6da1c7352386e12ddd46ce3d0bbb2310200fcc'
    )

def translate(text, from_code, to_code):
    from_code = str(from_code)
    to_code = str(to_code)

    if use_deepl:
        DEEPL_TOKEN = deepl_api_key
        print(f"Calling deepl with apikey: {DEEPL_TOKEN}")
        headers = {
            'Authorization': f'DeepL-Auth-Key {DEEPL_TOKEN}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = f'text={text}&target_lang={to_code.upper()}'
        translationResponse = requests.post(
            'https://api-free.deepl.com/v2/translate', headers=headers, data=data.encode('utf-8'))
        try:
            responseJSON = json.loads(
                translationResponse.content.decode('utf-8'))
            if "translations" in responseJSON:
                text_output = responseJSON['translations'][0]['text']
                print(f"DeepL translation: {text_output!r}")
                return text_output
        except Exception:
            print("Could not load json response from deepl.")
            print(f'Response content: {translationResponse}')
            print(f'Response content: {translationResponse.content}')
            print(traceback.format_exc())
            return ''
    else:
        if from_code == 'en' and to_code == 'ja':
            global fugu_translator
            if fugu_translator is None:
                fugu_translator = pipeline(
                    'translation', model='./models--staka--fugumt-en-ja/snapshots/2d6da1c7352386e12ddd46ce3d0bbb2310200fcc'
                )
            try:
                result = fugu_translator(text)
                return result[0]['translation_text']
            except Exception as e:
                print(traceback.format_exc())
                return ''
        else:
            print(
                f"No available model to translate from {from_code} to {to_code} (type={type(from_code)}, {type(to_code)})"
            )
            return ''

    # # Download and install Argos Translate package
    # argostranslate.package.update_package_index()
    # available_packages = argostranslate.package.get_available_packages()
    # package_to_install = next(
    #     filter(
    #         lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    #     )
    # )
    # argostranslate.package.install_from_path(package_to_install.download())

    # # print(f'{from_code}, {to_code}')
    # # Translate
    # translatedText = argostranslate.translate.translate(
    #     text, from_code, to_code)
    # return translatedText
