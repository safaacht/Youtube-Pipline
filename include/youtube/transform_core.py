import psycopg2


conn = psycopg2.connect(
    host="postgres",
    port=5432,
    database="youtube",
    user="postgres",
    password="postgres"
)

# print("Connected to PostgreSQL!")

cursor = conn.cursor()

# ===== insertion ====

cursor.execute("""
    INSERT INTO core.youtube_videos (
        video_id,
        title,
        published_at,
        duration_seconds,
        view_count,
        like_count,
        comment_count
    )
    SELECT
        s.video_id,
        s.title,
        s.published_at::TIMESTAMP,

        COALESCE((substring(s.duration FROM '(\d+)H'))::INTEGER, 0) * 3600
        + COALESCE((substring(s.duration FROM '(\d+)M'))::INTEGER, 0) * 60
        + COALESCE((substring(s.duration FROM '(\d+)S'))::INTEGER, 0),

        s.view_count::BIGINT,
        s.like_count::BIGINT,
        s.comment_count::BIGINT

    FROM staging.youtube_videos s
    WHERE NOT EXISTS (
        SELECT 1
        FROM core.youtube_videos c
        WHERE c.video_id = s.video_id
    );
""")

conn.commit()

# print("Transformation completed!")

# ===update====

cursor.execute("""
    UPDATE core.youtube_videos c
    SET
        title = s.title,
        published_at = s.published_at::TIMESTAMP,

        duration_seconds =
            COALESCE((substring(s.duration FROM '(\d+)H'))::INTEGER, 0) * 3600
            + COALESCE((substring(s.duration FROM '(\d+)M'))::INTEGER, 0) * 60
            + COALESCE((substring(s.duration FROM '(\d+)S'))::INTEGER, 0),

        view_count = s.view_count::BIGINT,
        like_count = s.like_count::BIGINT,
        comment_count = s.comment_count::BIGINT

    FROM staging.youtube_videos s
    WHERE c.video_id = s.video_id;
""")

# ===supression===

cursor.execute("""
    DELETE FROM core.youtube_videos c
    WHERE NOT EXISTS (
        SELECT 1
        FROM staging.youtube_videos s
        WHERE s.video_id = c.video_id
    );
""")

conn.commit()

print("Update synchronization completed!")
print("Delete synchronization completed!")

cursor.close()
conn.close()