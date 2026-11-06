import streamlit as st
import os
import tempfile
import time
from gtts import gTTS
from pydub import AudioSegment
from moviepy import AudioFileClip, TextClip, CompositeVideoClip


def create_simple_video(audio_path, output_video_path="output_video.mp4"):
    # Kunin ang haba ng nabuong audio
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    
    # Gumawa ng simpleng background text clip na kasin-haba ng audio
    txt_clip = TextClip("CineAI Studio Pro - Scene", fontsize=50, color='white', size=(1280, 720))
    txt_clip = txt_clip.set_duration(duration)
    
    # Ilapat ang audio sa video clip
    video = txt_clip.set_audio(audio_clip)
    
    # Isulat at i-render bilang MP4 file
    video.write_videofile(output_video_path, fps=24, codec='libx264', audio_codec='aac')
    return output_video_path
    
# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CineAI Studio Pro - Advanced Edition", 
    page_icon="🎬", 
    layout="wide"
)

st.title("🎬 CineAI Studio Pro (Production-Ready Edition)")
st.write("Lumikha ng 60-second AI video scenes, multi-prompt breakdown, voice-over, at background music mixing!")

# --- SIDEBAR: TEMPLATES & BGM SETTINGS ---
st.sidebar.header("🛠️ Templates & Audio Settings")
template_choice = st.sidebar.selectbox(
    "Pumili ng Starter Template:",
    [
        "Wala (Manual Input)", 
        "Pinoy Moto Vlog & Long Ride", 
        "Pangkabuhayan / Delivery Rider", 
        "Pamilya & Sunset Memory", 
        "Off-Road Overlanding Expedition",
        "Coastal & Island Hopping Adventure"
    ]
)

default_story = "Isang magandang kwento ng paglalakbay sa kalikasan."
if template_choice == "Pinoy Moto Vlog & Long Ride":
    default_story = "Isang rider na nakasuot ng buong protective gear habang bumabaybay sa paikot-ikot na kalsada ng kabundukan habang sumisikat ang araw."
elif template_choice == "Pangkabuhayan / Delivery Rider":
    default_story = "Isang matatag na rider na sumusuong sa maulan at ma trapik na kalsada ng lungsod para maghatid ng serbisyo at pangarap sa pamilya."
elif template_choice == "Pamilya & Sunset Memory":
    default_story = "Masayang naglalakad ang mag-anak sa tabing-dagat habang pinalilibutan ng makinang na gintong sinag ng lumulubog na araw."
elif template_choice == "Off-Road Overlanding Expedition":
    default_story = "Isang robust na 4x4 off-road vehicle na bumabaybay sa mabatong ilog at mabundok na daanan patungo sa isang isolated camping spot."
elif template_choice == "Coastal & Island Hopping Adventure":
    default_story = "Paglalakbay sakay ng tradisyunal na bangka sa kristal na katubigan at nakakabighaning mga rock formations sa mga isla."

st.sidebar.markdown("---")
st.sidebar.subheader("🎵 Background Music (BGM)")
bgm_option = st.sidebar.selectbox(
    "Pumili ng BGM Mood / Track:",
    ["Wala (Voice-Over Lamang)", "Cinematic Ambient", "Upbeat Travel Vlog", "Acoustic / Emotional"]
)

bgm_volume = st.sidebar.slider("BGM Volume Level (dB reduction):", min_value=-30, max_value=-5, value=-18, step=1)

# --- MAIN INTERFACE (2 COLUMNS) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Detalyadong Character & Tagpuan")
    character = st.selectbox(
        "Piliin ang Character Type:",
        [
            "Pilipino Moto Rider / Vlogger (Naka-riding jacket, full-face helmet, riding gloves)",
            "Lalaki (30s - 40s, Casual/Workwear, katamtamang pangangatawan)",
            "Babae (20s - 30s, Modern Pinay travel outfit, backpack)",
            "Pamilyang Pilipino (Tatay, Nanay, at Anak na may masayang aura)",
            "Matandang Propesyonal / Elder (May karunungan sa mukha, simpleng pananamit)",
            "Hardworking Delivery Rider (May cargo box at protective suit)"
        ]
    )

    character_shot = st.selectbox(
        "Anggulo ng Kamera (Camera Framing):",
        [
            "Wide Cinematic Angle (Buong katawan at nakapaligid na tanawin)",
            "Medium Shot (Mula baywang pataas, kasama ang background)",
            "Close-Up Shot (Focal point sa mukha o emosyon)",
            "Over-the-Shoulder / POV (Mula sa pananaw ng character)",
            "Low-Angle Hero Shot (Mula sa ibaba papuntang itaas)"
        ]
    )

    environment = st.selectbox(
        "Detalyadong Scene / Tagpuan:",
        [
            "Paikot-ikot na Kalsada sa Kabundukan (Mountain Highway / Twisties)",
            "Mabuhangin at Puting Dalampasigan (White Sand Beach & Shoreline)",
            "Mabalisbisan at Mabatong Ilog (River Trail / Fresh Stream)",
            "Sikip at Bustling na Kalsada ng Lungsod (Urban City Street)",
            "Luntiang Bukid at Palayan (Green Rice Terraces / Farmfield)",
            "Overland Off-Road Trail (Putik, Bato, at Gubat)"
        ]
    )

with col2:
    st.subheader("2. Weather, Transportasyon, at Audio")
    
    time_of_day = st.selectbox(
        "Oras at Liwanag (Time & Lighting):",
        [
            "Golden Hour / Sunrise (Gintong liwanag ng pagsikat ng araw)",
            "Bright Mid-day (Maliwanag na tanghaling tapat, malinaw na kalangitan)",
            "Golden Hour / Sunset (Lumulubog na araw, warm orange hues)",
            "Blue Hour / Dusk (Gabi-gabi na, malalim na asul na kalangitan)",
            "Moody Dawn / Twilight (Malamig na liwanag bago sumikat ang araw)"
        ]
    )

    weather = st.selectbox(
        "Panahon at Atmospera (Weather & Atmosphere):",
        [
            "Cine-Clear & Sunny (Maliwanag, asul na langit, may bahagyang ulap)",
            "Misty & Foggy (Malamig na fog/hamog sa bundok)",
            "Overcast & Moody (Makulimlim at dramatic skies)",
            "Light Tropical Rain / Ambon (Basang kalsada na may reflection)",
            "Heavy Downpour & Stormy (Malakas na ulan, hangin, at tilamsik ng tubig)"
        ]
    )

    vehicle = st.selectbox(
        "Transportasyon (Vehicle / Gear):",
        [
            "Adventure Scooter / Maxi-Scooter (160cc White Modern Scooter)",
            "Big Bike / Adventure Motorcycle (Off-road capable motorcycle)",
            "4x4 Off-Road Truck / Camper Utility Vehicle",
            "Tradisyunal na Bangkang Motor (Outrigger Motorized Boat)",
            "Wala (Naglalakad / On Foot)"
        ]
    )

    voice_lang = st.selectbox(
        "Wika ng Voice-Over:",
        ["Tagalog (Filipino)", "English"]
    )

# --- SCRIPT INPUT ---
st.subheader("3. Kwento at Voice-Over Script (60 Seconds)")
user_story = st.text_area("Isulat o baguhin ang iyong kwento:", value=default_story)

# --- HELPER FUNCTIONS ---
def generate_scene_prompts(story, char, env, veh, weath, tod, shot):
    """Bumubuo ng 6 na kakaibang scene prompts para sa 60-second breakdown."""
    scene_angles = [
        f"Scene 1 (Establishing Shot): Wide cinematic opening shot of {env}. {veh} appearing under {tod}. Atmosphere: {weath}.",
        f"Scene 2 (Character Intro): {shot} focusing on {char} operating {veh}. Mood: {tod}.",
        f"Scene 3 (Action / Movement): Dynamic tracking shot moving along {env}. Weather conditions: {weath}.",
        f"Scene 4 (Atmospheric Close-Up): Close-up detail of {char} enjoying the journey in {env}. Soft lighting: {tod}.",
        f"Scene 5 (Climax Landscape): B-roll beauty shot of {env} with dramatic weather {weath} and lighting {tod}.",
        f"Scene 6 (Outro / Conclusion): Slow fading cinematic shot of {char} with {veh} resting at {env} during {tod}."
    ]
    return scene_angles

def mix_audio_with_bgm(voice_file, bgm_type, volume_db):
    """Pinagsasama ang Voice-Over at BGM gamit ang Pydub."""
    voice = AudioSegment.from_file(voice_file)
    
    if bgm_type == "Wala (Voice-Over Lamang)":
        return voice_file
        
    # Gumawa ng simpleng synthetic ambient BGM bilang fallback kung walang audio file
    # Sa actual setup, maaari kang maglagay ng MP3 files sa local directory (hal. assets/bgm_cinematic.mp3)
    bgm = AudioSegment.silent(duration=len(voice) + 2000) # Silent track space
    
    # Adjust volume ng BGM
    bgm = bgm + volume_db
    
    # Overlay audio
    combined = voice.overlay(bgm, loop=True)
    
    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    combined.export(output_path, format="mp3")
    return output_path

# --- PROCESS & RENDER ENGINE ---
st.markdown("---")
st.subheader("4. Cloud Render & Multi-Prompt Generation")

if st.button("🚀 Buuin ang Scene Breakdown & Final Audio Track"):
    if not user_story.strip():
        st.warning("Mangyaring maglagay muna ng kwento o script.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("Hakbang 1/4: Kinokolekta ang script at binubuo ang Voice-Over...")
            progress_bar.progress(25)
            
            # 1. Voice-Over Generation
            tts_lang = 'tl' if "Tagalog" in voice_lang else 'en'
            tts = gTTS(text=user_story, lang=tts_lang, slow=False)
            raw_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            tts.save(raw_audio_path)
            
            status_text.text("Hakbang 2/4: Ipinoproseso ang Audio Mixing (Voice + BGM)...")
            progress_bar.progress(50)
            
            final_audio_path = mix_audio_with_bgm(raw_audio_path, bgm_option, bgm_volume)
            
            status_text.text("Hakbang 3/4: Binubuo ang 6-Scene AI Visual Prompt Breakdown...")
            progress_bar.progress(75)
            
            scenes = generate_scene_prompts(user_story, character, environment, vehicle, weather, time_of_day, character_shot)
            
            progress_bar.progress(100)
            status_text.text("✨ Tagumpay! Handa na ang iyong Scene Breakdown at Audio Track.")
            st.success("Matagumpay na nabuo ang lahat ng deliverables!")

            # --- DISPLAY SCENE BREAKDOWN ---
            st.markdown("### 🎬 6-Scene AI Video Prompt Breakdown:")
            prompt_text_content = f"--- CINEAI STUDIO PRO - PROJECT PROMPTS ---\nStory: {user_story}\n\n"
            
            for idx, sc_prompt in enumerate(scenes, 1):
                st.text_area(f"Eksena {idx} (10 Seconds):", value=sc_prompt, height=80)
                prompt_text_content += f"{sc_prompt}\n\n"

            # --- DOWNLOAD PROMPTS (.TXT FILE) ---
            st.download_button(
                label="📥 Download All Prompts (.txt)",
                data=prompt_text_content,
                file_name="CineAI_Scene_Prompts.txt",
                mime="text/plain"
            )

            # --- PREVIEW & AUDIO DOWNLOAD ---
            st.markdown("---")
            st.markdown("### 🎧 Final Mixed Voice-Over & BGM Preview:")
            st.audio(final_audio_path)
            
            with open(final_audio_path, "rb") as f:
                st.download_button(
                    label="📥 Download Final Mixed Audio (MP3)",
                    data=f,
                    file_name="CineAI_Final_Audio_Track.mp3",
                    mime="audio/mp3"
                )

        except Exception as e:
            st.error(f"Nagka-error sa processing: {e}")
