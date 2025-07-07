import google.auth
import os

print("Attempting to find Google Cloud credentials...")
try:
    credentials, project = google.auth.default()
    print(f"SUCCESS! Credentials found for project: {project}")
    print(f"Credentials type: {type(credentials)}")
    print(f"Credential scopes: {credentials.scopes}")
    # Optional: Check GOOGLE_APPLICATION_CREDENTIALS env var (should be empty if ADC is working as expected)
    print(f"GOOGLE_APPLICATION_CREDENTIALS env var: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")

except Exception as e:
    print(f"ERROR! Could not find default credentials: {e}")
    print("Please ensure you have run 'gcloud auth application-default login' and restarted your terminal.")