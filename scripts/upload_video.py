#!/usr/bin/env python3
import os
import argparse
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN_FILE = "token.pickle"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError("token.pickle が見つかりません。先に get_credentials.py を実行してください。")
    with open(TOKEN_FILE, "rb") as f:
        creds = pickle.load(f)
    return build("youtube", "v3", credentials=creds)

def upload_video(file_path, title, description="", tags=None, category_id="22", privacy_status="unlisted"):
    youtube = get_authenticated_service()
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"アップロード進捗: {int(status.progress() * 100)}%")

    video_id = response["id"]
    print("✅ アップロード完了！")
    print(f"📺 視聴URL: https://youtu.be/{video_id}")
    return video_id

def parse_args():
    parser = argparse.ArgumentParser(description="YouTube に動画をアップロードするスクリプト")
    parser.add_argument("file", help="アップロードする動画ファイルのパス")
    parser.add_argument("-t", "--title", required=True, help="動画のタイトル")
    parser.add_argument("-d", "--description", default="", help="動画の説明文")
    parser.add_argument("--tags", nargs="*", help="スペースまたはカンマ区切りでタグを指定")
    parser.add_argument("-c", "--category", default="22", help="カテゴリ ID（デフォルトは People & Blogs）")
    parser.add_argument("-p", "--privacy", choices=["public", "unlisted", "private"], default="unlisted", help="公開設定")
    return parser.parse_args()

def main():
    args = parse_args()
    tags = []
    if args.tags:
        raw = " ".join(args.tags)
        tags = [tag.strip() for tag in raw.replace(",", " ").split() if tag.strip()]

    upload_video(
        file_path=args.file,
        title=args.title,
        description=args.description,
        tags=tags,
        category_id=args.category,
        privacy_status=args.privacy,
    )

if __name__ == "__main__":
    main()

