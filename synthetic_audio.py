# synthetic_audio.py - Updated version
import numpy as np
import soundfile as sf
import os

def generate_clean_audio(filename="clean_speech.wav", duration=5, sample_rate=16000):
    """Generate PURE CLEAN audio (no noise)"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Clean speech-like signal
    clean = 0.5 * np.sin(2 * np.pi * 500 * t)
    clean += 0.3 * np.sin(2 * np.pi * 1000 * t)
    clean += 0.2 * np.sin(2 * np.pi * 1500 * t)
    
    # Normalize
    clean = clean / np.max(np.abs(clean)) * 0.9
    
    sf.write(filename, clean, sample_rate)
    print(f"✅ CLEAN audio: {filename}")
    return filename

def generate_noisy_audio(filename="noisy_speech.wav", duration=5, sample_rate=16000, noise_level=0.2):
    """Generate NOISY audio for testing noise reduction"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Clean signal
    clean = 0.5 * np.sin(2 * np.pi * 500 * t)
    clean += 0.3 * np.sin(2 * np.pi * 1000 * t)
    
    # Add noise
    noise = noise_level * np.random.randn(len(t))
    
    # Mix
    noisy = clean + noise
    noisy = noisy / np.max(np.abs(noisy)) * 0.9
    
    sf.write(filename, noisy, sample_rate)
    print(f"✅ NOISY audio: {filename} (noise level: {noise_level})")
    return filename

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    print("="*50)
    print("GENERATING TEST AUDIO FILES")
    print("="*50)
    
    # 1. Generate CLEAN audio (no noise)
    generate_clean_audio("uploads/clean_sample.wav")
    
    # 2. Generate NOISY audio (with different noise levels)
    generate_noisy_audio("uploads/noisy_light.wav", noise_level=0.1)  # 10% noise
    generate_noisy_audio("uploads/noisy_medium.wav", noise_level=0.3)  # 30% noise
    generate_noisy_audio("uploads/noisy_heavy.wav", noise_level=0.5)  # 50% noise
    
    print("\n" + "="*50)
    print("FILES CREATED:")
    print("📁 uploads/clean_sample.wav - PURE CLEAN (no noise)")
    print("📁 uploads/noisy_light.wav - 10% noise")
    print("📁 uploads/noisy_medium.wav - 30% noise")
    print("📁 uploads/noisy_heavy.wav - 50% noise")
    print("="*50)