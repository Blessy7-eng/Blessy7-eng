# 🎬 PulsePoint AI: Viral Reel Engine

**PulsePoint AI** is an automated video-to-reel engine built for the **ByteSize Sage Hackathon**. It transforms long-form educational content into high-impact, 9:16 vertical reels using local audio analysis and speech-to-text.

## 🚀 The Core Problem
During the hackathon, we found that relying on cloud-based LLMs (like Gemini) created a massive bottleneck due to strict rate limits and `429 RESOURCE_EXHAUSTED` errors. We needed a solution that was fast, free, and worked 100% offline.

## ✨ Our Solution: The Local Pulse Engine
PulsePoint AI bypasses cloud limitations by using a **Hybrid Local Processing** approach:

* **Audio Energy Peak Detection**: Uses `librosa` to analyze the mathematical "Pulse" of the audio. It detects loudness spikes (RMS analysis) to automatically find where the speaker is most engaging.
* **Local Transcription**: Runs OpenAI's **Whisper (Tiny)** model locally to generate timestamped transcripts without any API keys.
* **Smart 9:16 Cropping**: Automatically centers and crops 16:9 landscape video into mobile-ready vertical reels using `MoviePy`.
* **Dynamic Captions**: Synchronizes Whisper’s timestamps to overlay bold, social-media-style captions directly onto the video.

## 🛠️ Tech Stack
* **Frontend**: Streamlit
* **Audio Analysis**: Librosa & NumPy
* **Transcription**: OpenAI Whisper (Local)
* **Video Engine**: MoviePy
* **Environment**: Python 3.9+

## ⚙️ Installation

### Prerequisites
1.  **ImageMagick**: Required for rendering text captions.
    * *Windows*: Install ImageMagick and update the `IMAGEMAGICK_BINARY` path in `main.py`.

### Setup
1.  **Clone the Repo**:
    ```bash
    git clone [https://github.com/Blessy7-eng/ByteSize_Sage-Hackathon.git](https://github.com/Blessy7-eng/ByteSize_Sage-Hackathon.git)
    cd ByteSize_Sage-Hackathon
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the App**:
    ```bash
    streamlit run main.py
    ```

## 🧠 Why It Wins
* **Resilience**: No API keys, no quotas, and no internet required for processing.
* **Speed**: By using the Whisper "tiny" model, we generate reels in seconds, not minutes.
* **User Focus**: Transforms "boring" lectures into "viral" nuggets with a single click.

---
**Developed for ByteSize Sage Hackathon 2026**
