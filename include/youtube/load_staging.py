import json
import psycopg2


def load_to_staging() :

    conn = psycopg2.connect(
        host = "postgres",
        port = 5432,
        database = "youtube",
        user = "postgres",
        password = "postgres"
    )


    with open("/opt/airflow/data/youtube_SAFAA_2026-09-15.json", "r", encoding="utf-8") as file:
        videos = json.load(file)


    cursor = conn.cursor()

    for video in videos:
        cursor.execute("""
            INSERT INTO staging.youtube_videos
            (video_id, title, published_at, duration, view_count, like_count, comment_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (video_id) DO NOTHING
            """, (
            video["videoId"],
            video["title"],
            video["publishedAt"],
            video["duration"],
            video["viewCount"],
            video["likeCount"],
            video["commentCount"]
        ))

    conn.commit()

    cursor.close()
    conn.close()

    print("Videos inserted into Staging:", len(videos))    

    # return videos

print(load_to_staging())