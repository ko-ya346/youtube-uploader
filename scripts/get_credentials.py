from google.cloud import secretmanager
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def fetch_client_secret(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return json.loads(response.payload.data)

def save_token_from_secret(project_id, secret_id, output_json="client_secret.json", token_file="token.pickle"):
    # Secret Manager から取得 → 一時保存
    secret = fetch_client_secret(project_id, secret_id)
    with open(output_json, "w") as f:
        json.dump(secret, f)

    # ブラウザで認証 → token.pickle を生成
    flow = InstalledAppFlow.from_client_secrets_file(output_json, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(token_file, "wb") as f:
        pickle.dump(creds, f)

    print(f"認証完了 → {token_file} に保存されました")

if __name__ == "__main__":
    save_token_from_secret(
        project_id="youtube-uploader",
        secret_id="youtube-oauth-client"
    )

