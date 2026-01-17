import streamlit as st
import moviepy.editor as mp
from moviepy.video.fx.all import crop
from moviepy.config import change_settings
import whisper
import librosa
import numpy as np
import os

# --- 1. CONFIGURATION ---
# Updated path based on your screenshots showing version 7.1.2
IMAGEMAGICK_PATH = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_PATH})


def create_vertical_reel(full_video_path, start, end, segments, output_name):
    """Crops video to 9:16 with a fallback to skip captions if ImageMagick fails."""
    clip = mp.VideoFileClip(full_video_path).subclip(start, end)

    # --- A. CROP TO 9:16 (Always Works) ---
    w, h = clip.size
    target_ratio = 9 / 16
    target_w = int(h * target_ratio)
    x_center = w / 2
    final_clip = crop(clip, x_center=x_center, y1=0, width=target_w, height=h)

    try:
        # --- B. ATTEMPT DYNAMIC CAPTIONS ---
        caption_clips = []
        relevant_segments = [s for s in segments if s['start'] >= start and s['end'] <= end]

        for s in relevant_segments:
            duration = s['end'] - s['start']
            if duration <= 0: continue

            txt = mp.TextClip(
                s['text'].strip().upper(),
                fontsize=target_w * 0.07,
                color='yellow',
                font='Arial-Bold',
                method='caption',
                align='center',
                size=(target_w * 0.8, None)
            ).set_start(s['start'] - start).set_duration(duration).set_position(('center', h * 0.8))
            caption_clips.append(txt)

        # Composite: Video + Captions
        result = mp.CompositeVideoClip([final_clip] + caption_clips)
        result.write_videofile(output_name, codec="libx264", audio_codec="aac", fps=24, logger=None)

    except Exception as e:
        # --- C. FALLBACK: SAFE MODE (No Captions) ---
        st.warning("⚠️ Captions failed (ImageMagick error). Generating vertical crop only.")
        final_clip.write_videofile(output_name, codec="libx264", audio_codec="aac", fps=24, logger=None)

    finally:
        clip.close()


def get_local_segments(audio_path, num_segments=3):
    """Detects high-energy audio peaks to find viral moments."""
    y, sr = librosa.load(audio_path)
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr)

    segments = []
    sorted_indices = np.argsort(rms)[::-1]
    for idx in sorted_indices:
        peak_time = times[idx]
        if not any(abs(peak_time - s[0]) < 60 for s in segments):
            start = max(0, int(peak_time - 5))
            end = min(int(times[-1]), start + 30)
            segments.append((start, end))
        if len(segments) >= num_segments: break
    return sorted(segments)


# --- 2. STREAMLIT UI ---
st.set_page_config(page_title="PulsePoint AI", page_icon="🎬", layout="wide")
st.title("🎬 PulsePoint AI: Viral Reel Engine")

if 'full_result' not in st.session_state:
    st.session_state.full_result = None

uploaded_file = st.file_uploader("Upload Video", type=["mp4"])

if uploaded_file:
    temp_path = "input_video.mp4"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("🚀 Generate 9:16 Viral Reels"):
        with st.spinner("Analyzing Audio & Transcribing..."):
            # Ensure file is ready for MoviePy
            video_input = mp.VideoFileClip(temp_path)
            audio_path = "temp_audio.wav"
            video_input.audio.write_audiofile(audio_path, fps=16000, codec='pcm_s16le', logger=None)
            video_input.close()

            # Local Analysis (No API)
            model = whisper.load_model("tiny")
            st.session_state.full_result = model.transcribe(audio_path)
            segments_to_cut = get_local_segments(audio_path)

        st.divider()
        cols = st.columns(len(segments_to_cut))

        for i, (start, end) in enumerate(segments_to_cut):
            output_name = f"reel_{i + 1}.mp4"
            with st.spinner(f"Creating Reel {i + 1}..."):
                create_vertical_reel(temp_path, start, end, st.session_state.full_result['segments'], output_name)
                with cols[i]:
                    st.video(output_name)
                    st.download_button(f"Download Reel {i + 1}", open(output_name, "rb"), file_name=output_name)
        st.balloons()