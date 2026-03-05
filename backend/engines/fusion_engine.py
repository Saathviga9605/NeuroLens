def calculate_csi(behavioral_score, voice_score=None, nlp_score=None):
    """
    Weighted Fusion:
    0.3 behavioral
    0.3 voice
    0.4 nlp
    """

    voice_score = voice_score if voice_score is not None else 50
    nlp_score = nlp_score if nlp_score is not None else 50

    csi = (
        0.3 * behavioral_score +
        0.3 * voice_score +
        0.4 * nlp_score
    )

    return round(csi, 2)