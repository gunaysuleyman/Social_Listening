from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv('YOUTUBE_API_KEY')
if not API_KEY:
    raise ValueError("Hata: YOUTUBE_API_KEY bulunamadı! Lütfen .env dosyasını kontrol edin.")

categories = {
    "Müzik": "10",
    "Oyun": "20",
    "Filmler": "1",
    "Genel": None  
}

def get_trending_videos(api_key, category_id=None, region_code='TR', max_results=10):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.videos().list(
        part='snippet,statistics',  
        chart='mostPopular',
        regionCode=region_code,
        videoCategoryId=category_id,  
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response['items']:
        title = item['snippet']['title']
        description = item['snippet']['description']
        published_at = item['snippet']['publishedAt']
        view_count = item['statistics'].get('viewCount', 0)
        like_count = item['statistics'].get('likeCount', 0)
        comment_count = item['statistics'].get('commentCount', 0)

        videos.append({
            "Başlık": title,
            "Açıklama": description,
            "Yüklenme Tarihi": published_at,
            "İzlenme Sayısı": int(view_count),
            "Beğeni Sayısı": int(like_count),
            "Yorum Sayısı": int(comment_count)
        })
    return videos


all_videos = []
for category_name, category_id in categories.items():
    videos = get_trending_videos(API_KEY, category_id=category_id)
    for video in videos:
        video["Kategori"] = category_name
    all_videos.extend(videos)


df = pd.DataFrame(all_videos)


excel_file = "YouTube_Trend_Videolar.xlsx"
df.to_excel(excel_file, index=False)

print(f"Veriler '{excel_file}' dosyasına başarıyla aktarıldı.")