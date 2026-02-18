import requests
from pathlib import Path
import sys

# Constants
API_URL = "http://localhost:8000/api/v1"
TEST_IMAGE_PATH = Path("testScripts/TextOcr.png") # Updated to use existing image

def test_extract(image_path):
    print(f"\nTesting /extract with {image_path}...")
    url = f"{API_URL}/ocr/extract"
    files = {'file': open(image_path, 'rb')}
    data = {'lang': 'eng'}
    
    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("SUCCESS:")
            print(response.json())
            return True
        else:
            print(f"FAILED: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_analyze(image_path):
    print(f"\nTesting /analyze with {image_path}...")
    url = f"{API_URL}/ocr/analyze"
    files = {'file': open(image_path, 'rb')}
    data = {'lang': 'eng'}
    
    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("SUCCESS:")
            # Print a summary of the response to avoid flooding console
            res_json = response.json()
            nlp_data = res_json.get('nlp_analysis', {})
            print(f"Text length: {len(res_json.get('text', ''))}")
            if nlp_data:
                print(f"Entities found: {len(nlp_data.get('entities', []))}")
                print(f"Sentences detected: {nlp_data.get('num_sentences', 0)}")
            return True
        else:
            print(f"FAILED: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_analyze_text(image_path):
    print(f"\nTesting /analyze/text with {image_path}...")
    url = f"{API_URL}/ocr/analyze/text"
    files = {'file': open(image_path, 'rb')}
    data = {'lang': 'eng'}
    
    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("SUCCESS:")
            print("-" * 20)
            print(response.text) # Print the report
            print("-" * 20)
            return True
        else:
            print(f"FAILED: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_analyze_html(image_path):
    print(f"\nTesting /analyze/html with {image_path}...")
    url = f"{API_URL}/ocr/analyze/html"
    files = {'file': open(image_path, 'rb')}
    data = {'lang': 'eng'}
    
    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("SUCCESS:")
            output_file = "test_output.html"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"HTML report saved to {output_file}")
            return True
        else:
            print(f"FAILED: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_autocorrect(image_path):
    print(f"\nTesting /analyze/text with autocorrect=True for {image_path}...")
    url = f"{API_URL}/ocr/analyze/text"
    files = {'file': open(image_path, 'rb')}
    data = {'lang': 'eng', 'autocorrect': 'true'}
    
    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            if "CORRECTED TEXT" in response.text:
                print("SUCCESS: 'CORRECTED TEXT' section found.")
                
                # Check for asterisks
                if "*" in response.text:
                    print("SUCCESS: Autocorrect highlighting (*) found.")
                    return True
                else:
                    print("WARNING: 'CORRECTED TEXT' found but no asterisks (*). Maybe no corrections were needed?")
                    # For now, we consider it a pass if the section exists, but warn about asterisk
                    return True
            else:
                print("FAILED: 'CORRECTED TEXT' section NOT found.")
                print(response.text[:500]) # Print beginning of response
                return False
        else:
            print(f"FAILED: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_image_enhancement(image_path):
    print(f"\nTesting /extract with contrast=2.0 for {image_path}...")
    url = f"{API_URL}/ocr/extract"
    files = {'file': open(image_path, 'rb')}
    data = {'lang': 'eng', 'contrast': '2.0', 'brightness': '1.2'}
    
    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("SUCCESS: Image enhancement parameters accepted.")
            return True
        else:
            print(f"FAILED: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_processed_image_saved():
    print("\nTesting if processed image is saved...")
    output_dir = Path("processedimages")
    # Count files before
    files_before = len(list(output_dir.glob("*.png"))) if output_dir.exists() else 0
    
    # Trigger image processing
    test_image_enhancement(TEST_IMAGE_PATH)
    
    # Count files after
    files_after = len(list(output_dir.glob("*.png"))) if output_dir.exists() else 0
    
    if files_after > files_before:
        print(f"SUCCESS: New file created in {output_dir}. Total files: {files_after}")
        return True
    else:
        print(f"FAILED: No new file created in {output_dir}.")
        return False

if __name__ == "__main__":
    if not TEST_IMAGE_PATH.exists():
        print(f"Warning: Test image not found at {TEST_IMAGE_PATH}")
        print("Please check the path or run with a valid image.")
        # Try to find any png/jpg in current dir or testScripts
        possible_images = list(Path('.').glob('*.png')) + list(Path('testScripts').glob('*.png')) + list(Path('.').glob('*.jpg'))
        if possible_images:
            TEST_IMAGE_PATH = possible_images[0]
            print(f"Using found image: {TEST_IMAGE_PATH}")
        else:
            print("No images found to test with.")
            sys.exit(1)

    print("Starting verification...")
    # user needs to have the server running for this to work
    # We can try to assume it's running or guide the user
    try:
        requests.get("http://localhost:8000/docs", timeout=2)
    except requests.exceptions.ConnectionError:
        print("Error: FastAPI server is not running on localhost:8000")
        print("Please run: python app/main.py")
        sys.exit(1)

    ocr_success = test_extract(TEST_IMAGE_PATH)
    nlp_success = test_analyze(TEST_IMAGE_PATH)
    report_success = test_analyze_text(TEST_IMAGE_PATH)
    html_success = test_analyze_html(TEST_IMAGE_PATH)
    autocorrect_success = test_autocorrect(TEST_IMAGE_PATH)
    enhancement_success = test_image_enhancement(TEST_IMAGE_PATH)
    file_save_success = test_processed_image_saved()
    
    if ocr_success and nlp_success and report_success and html_success and autocorrect_success and enhancement_success and file_save_success:
        print("\nVerification Passed!")
    else:
        print("\nVerification Failed.")
