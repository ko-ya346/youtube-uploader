terraform {
  required_version = ">= 1.2"
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region = var.region
}

# youtube data api v3 有効化
resource "google_project_service" "youtube_api" {
  service = "youtube.googleapis.com"
}

# secret manager に oauth クライアント情報を格納
resource "google_secret_manager_secret" "youtube_oauth" {
  secret_id = "youtube-oauth-client"
  replication {
    automatic = true
  }
  depends_on = [ google_project_service.youtube_api ]
}

resource "google_secret_manager_secret_version" "youtube_oauth_version" {
  secret = google_secret_manager_secret.youtube_oauth.id
  secret_data = file("${path.module}/secrets/client_secret.json")
}

  

