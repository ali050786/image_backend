import requests
import base64

# Load test image
with open("D:/canva/a7000b9b5bbc6820e4540e3da7e01152.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

# Make API request
response = requests.post(
    'http://localhost:5000/api/background/remove',
    json={
        'imageData': f"data:image/jpeg;base64,{encoded_string}"
    }
)

# Check response
if response.status_code == 200:
    result = response.json()
    if result['success']:
        # Save the result
        img_data = base64.b64decode(result['data']['image'].split(',')[1])
        with open('result.png', 'wb') as f:
            f.write(img_data)
        print("Success! Result saved as result.png")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
else:
    print(f"Error {response.status_code}: {response.text}")