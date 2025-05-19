output "oauth_secret_name" {
  description = "Secret Manager に格納された OAuth クライアント情報のリソース名"
  value = google_secret_manager_secret.youtube_oauth.name
}
