# youtube uploader
YouTube に動画をアップロードする。  

# 前提
- Google Cloud プロジェクトがある  
- YouTube チャンネルを所有している

# セットアップ手順
## 1. クローン  

```
git clone https://github.com/ko-ya346/youtube-uploader.git
cd youtube-uploader
```

## 2. OAuth クライアント情報を登録
1. Google Cloud Console にログイン  
1. OAuth クライアントID をデスクトップアプリとして作成  
1. JSON ダウンロード  
1. `terraform/secrets/client_secret.json` として配置  

## 3. Terraform で Secret Manager に登録  
```
cd terraform
terraform init
terraform apply -var="project_id=your-project-id"
```

## 4. OAuth 同意画面の設定  
1. Cloud Console で "OAuth 同意画面"を開く  
1. "外部"ユーザーを選択  
1. 「テストユーザー」に自分の Gmail アカウント(YouTube アカウント)を追加  

## 5. OAuth の診断トークンを発行  
```
python scripts/get_cretentials.py
```
## 6. 動画をアップロード  
```
python scripts/upload_video.py \
  ./videos/myvideo.mp4 \
  -t "家族旅行" \
  -d "2025年GW" \
  --tags 家族 旅行 \
  -p unlisted
```
