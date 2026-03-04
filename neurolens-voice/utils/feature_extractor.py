"""
feature_extractor.py
--------------------
Extracts paralinguistic features from raw audio that correlate with
cognitive stress, emotional state, and mental health markers.

Features extracted:
  - MFCCs (Mel-frequency cepstral coefficients) — vocal tract shape / tone quality
  - Pitch (F0) — fundamental frequency, flatness = emotional numbing
  - Speech rate — slowing down = depression marker
  - Energy / RMS — low energy = low affect
  - Zero-crossing rate — voice tremor / irregularity
  - Spectral features — brightness, bandwidth, rolloff
  - Pause ratio — hesitation, cognitive load
  - Jitter & shimmer proxies — vocal stability
"""

import librosa
import librosa.feature
import numpy as np
from typing import Dict, Any
import io


class VoiceFeatureExtractor:
    """
    Extracts a full set of paralinguistic features from an audio signal.
    All features are normalized to [0, 1] where applicable.
    """

    def __init__(self, sample_rate: int = 22050):
        self.sr = sample_rate

    def load_audio(self, audio_bytes: bytes) -> np.ndarray:
        """Load audio from raw bytes — handles wav, mp3, m4a, ogg, webm."""
        # First try librosa directly
        try:
            audio_buffer = io.BytesIO(audio_bytes)
            y, sr = librosa.load(audio_buffer, sr=self.sr, mono=True)
            return y
        except Exception:
            pass

        # Fallback: use pydub to convert (handles m4a, mp3, webm, etc.)
        from pydub import AudioSegment
        audio_buffer = io.BytesIO(audio_bytes)
        audio = AudioSegment.from_file(audio_buffer)
        audio = audio.set_channels(1).set_frame_rate(self.sr)
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        y, sr = librosa.load(wav_buffer, sr=self.sr, mono=True)
        return y

    # ------------------------------------------------------------------
    # Individual feature extractors
    # ------------------------------------------------------------------

    def extract_mfcc(self, y: np.ndarray, n_mfcc: int = 13) -> Dict[str, float]:
        """
        MFCCs capture vocal tract shape and tone quality.
        High variance in MFCCs over time suggests emotional instability.
        """
        mfcc = librosa.feature.mfcc(y=y, sr=self.sr, n_mfcc=n_mfcc)
        return {
            "mfcc_mean": float(np.mean(mfcc)),
            "mfcc_std": float(np.std(mfcc)),
            "mfcc_variance": float(np.var(mfcc)),
            "mfcc_delta_mean": float(np.mean(librosa.feature.delta(mfcc))),
        }

    def extract_pitch(self, y: np.ndarray) -> Dict[str, float]:
        """
        Pitch (F0) — fundamental frequency.
        Depressed speech tends to be lower pitch with less variation (flat affect).
        """
        f0, voiced_flag, _ = librosa.pyin(
            y,
            fmin=librosa.note_to_hz("C2"),
            fmax=librosa.note_to_hz("C7"),
            sr=self.sr
        )

        # Only use voiced frames
        voiced_f0 = f0[voiced_flag] if voiced_flag is not None else f0
        voiced_f0 = voiced_f0[~np.isnan(voiced_f0)] if len(voiced_f0) > 0 else np.array([0.0])

        if len(voiced_f0) == 0:
            voiced_f0 = np.array([0.0])

        pitch_mean = float(np.mean(voiced_f0))
        pitch_std = float(np.std(voiced_f0))
        voiced_ratio = float(np.sum(voiced_flag) / len(voiced_flag)) if voiced_flag is not None else 0.0

        return {
            "pitch_mean_hz": pitch_mean,
            "pitch_std": pitch_std,
            # Low variation = flatter speech = depression marker
            "pitch_variation": min(pitch_std / (pitch_mean + 1e-6), 1.0),
            "voiced_ratio": voiced_ratio,
        }

    def extract_energy(self, y: np.ndarray) -> Dict[str, float]:
        """
        RMS energy — overall loudness and vitality.
        Low energy / low affect is a key indicator of depression.
        """
        rms = librosa.feature.rms(y=y)[0]
        return {
            "energy_mean": float(np.mean(rms)),
            "energy_std": float(np.std(rms)),
            # Energy variance: flat energy = flat affect
            "energy_flatness": 1.0 - min(float(np.std(rms) / (np.mean(rms) + 1e-6)), 1.0),
        }

    def extract_speech_rate(self, y: np.ndarray) -> Dict[str, float]:
        """
        Estimates speech rate via onset detection.
        Slower speech rate is correlated with cognitive fatigue and depression.
        """
        duration = librosa.get_duration(y=y, sr=self.sr)
        onsets = librosa.onset.onset_detect(y=y, sr=self.sr, units="time")
        n_onsets = len(onsets)

        # Syllables per second proxy
        speech_rate = n_onsets / duration if duration > 0 else 0.0

        return {
            "speech_rate_sps": float(speech_rate),   # syllables per second
            "total_onsets": int(n_onsets),
            "duration_seconds": float(duration),
        }

    def extract_zero_crossing_rate(self, y: np.ndarray) -> Dict[str, float]:
        """
        ZCR captures voice roughness, breathiness, and tremor.
        High irregular ZCR can indicate voice tremor from anxiety/stress.
        """
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        return {
            "zcr_mean": float(np.mean(zcr)),
            "zcr_std": float(np.std(zcr)),
        }

    def extract_spectral_features(self, y: np.ndarray) -> Dict[str, float]:
        """
        Spectral features describe the 'color' and texture of voice.
        - Centroid: brightness of voice
        - Bandwidth: spread of frequencies
        - Rolloff: ratio of high-frequency content
        """
        centroid = librosa.feature.spectral_centroid(y=y, sr=self.sr)[0]
        bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=self.sr)[0]
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=self.sr)[0]
        flatness = librosa.feature.spectral_flatness(y=y)[0]

        return {
            "spectral_centroid_mean": float(np.mean(centroid)),
            "spectral_bandwidth_mean": float(np.mean(bandwidth)),
            "spectral_rolloff_mean": float(np.mean(rolloff)),
            "spectral_flatness_mean": float(np.mean(flatness)),
        }

    def extract_pause_ratio(self, y: np.ndarray, threshold_db: float = -40.0) -> Dict[str, float]:
        """
        Estimates ratio of silence/pauses in the audio.
        Higher pause ratio = more hesitation = cognitive load or depression.
        """
        intervals = librosa.effects.split(y, top_db=abs(threshold_db))
        speech_duration = sum([(end - start) for start, end in intervals]) / self.sr
        total_duration = librosa.get_duration(y=y, sr=self.sr)
        pause_ratio = 1.0 - (speech_duration / total_duration) if total_duration > 0 else 0.0

        return {
            "pause_ratio": float(np.clip(pause_ratio, 0, 1)),
            "speech_segments": int(len(intervals)),
        }

    # ------------------------------------------------------------------
    # Master extractor
    # ------------------------------------------------------------------

    def extract_all(self, audio_bytes: bytes) -> Dict[str, Any]:
        """
        Full extraction pipeline.
        Returns a flat dictionary of all paralinguistic features.
        """
        y = self.load_audio(audio_bytes)

        features = {}
        features.update(self.extract_mfcc(y))
        features.update(self.extract_pitch(y))
        features.update(self.extract_energy(y))
        features.update(self.extract_speech_rate(y))
        features.update(self.extract_zero_crossing_rate(y))
        features.update(self.extract_spectral_features(y))
        features.update(self.extract_pause_ratio(y))

        return features
