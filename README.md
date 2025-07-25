# Whisper API Wrapper (FastAPI + Faster-Whisper)

This project provides a lightweight HTTP wrapper around the [faster-whisper](https://github.com/guillaumekln/faster-whisper) transcription engine using FastAPI. It supports both file upload and URL-based transcription with optional translation and language specification.

## 🚀 Features

- 🎙️ Transcribe audio files using Whisper (`tiny` model by default)
- 📤 Supports direct file uploads (`/transcribe`)
- 🌐 Supports public or presigned audio URLs (`/transcribe-url`)
- 🔐 Token-based authentication via `Authorization: Bearer <token>`
- 🌍 Language selection and translation to English
- 🐳 Dockerized and ready to deploy

---

## 🧪 Endpoints

### `POST /transcribe`

Transcribe an uploaded audio file.

#### Headers:
```
Authorization: Bearer changeme123
```

#### Body (form-data):
| Field | Type | Description |
|-------|------|-------------|
| file | File | Audio file (.mp3, .wav, etc.) |
| language (optional) | String | Language code (e.g., 'en', 'th') |
| translate (optional) | Boolean | Translate to English (`true`/`false`) |

### `POST /transcribe-url`

Transcribe an audio file by providing a URL (e.g. MinIO presigned URL).

#### Headers:
```
Authorization: Bearer changeme123
Content-Type: application/json
```

#### JSON Body:
```json
{
  "url": "https://your-minio-domain/bucket/audio.mp3"
}
```

Optional query params:
- `language=en`
- `translate=true`

---

## 🐳 Docker Usage

### Build & Run
```bash
docker build -t whisper-api .
docker run -p 10300:10300 -e WHISPER_API_TOKEN=changeme123 whisper-api
```

### Docker Compose
Add to your `docker-compose.yml`:
```yaml
whisper-api:
  build: ./whisper-wrapper
  container_name: whisper-api
  networks:
    - proxy
  ports:
    - "10300:10300"
  environment:
    - WHISPER_API_TOKEN=changeme123
  restart: unless-stopped
```

---

## 📁 Recommended Usage With MinIO

- Upload audio files to MinIO via n8n or API
- Generate a presigned URL
- Call `/transcribe-url` with that URL
- Optional: send the transcript back to MinIO or store in DB

---

## 🛡️ Security

- Uses `Authorization: Bearer <token>` for simple auth
- Change `WHISPER_API_TOKEN` in production

---

## 📄 License

MIT License. Built using [FastAPI](https://fastapi.tiangolo.com/) and [faster-whisper](https://github.com/guillaumekln/faster-whisper).
