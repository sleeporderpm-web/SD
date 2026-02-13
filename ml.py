from typing import Dict, Tuple


def classify(inputs: Dict) -> Tuple[str, int]:
    age = int(inputs.get("age", 0))
    stress = int(inputs.get("stress", 0))
    bp = float(inputs.get("blood_pressure", 0))
    hr = int(inputs.get("heart_rate", 0))
    duration = float(inputs.get("sleep_duration", 0))
    bmi = str(inputs.get("bmi_category", "")).lower()
    snore = int(inputs.get("snoring_frequency", 0))
    hours_work = int(inputs.get("working_hours", 0))

    osa_score = 0
    if bmi in {"overweight", "obese"}:
        osa_score += 2
    if snore >= 5:
        osa_score += 2
    if bp >= 140:
        osa_score += 1
    if hr >= 90:
        osa_score += 1
    if duration <= 5:
        osa_score += 1

    insomnia_score = 0
    if duration <= 4:
        insomnia_score += 2
    if stress >= 8:
        insomnia_score += 2
    if hours_work >= 10:
        insomnia_score += 1

    deprivation_score = 0
    if duration < 6:
        deprivation_score += 2
    if hours_work >= 9:
        deprivation_score += 1
    if stress >= 7:
        deprivation_score += 1

    if osa_score >= 5:
        return "High Risk: Possible Obstructive Sleep Apnea", 3
    if insomnia_score >= 4:
        return "High Risk: Chronic Insomnia", 3
    if deprivation_score >= 3:
        return "Moderate Risk: Sleep Deprivation", 2
    if 7 <= duration <= 9 and stress <= 6 and snore <= 2:
        return "Normal", 0
    if deprivation_score >= 2:
        return "Moderate Risk: Sleep Deprivation", 2
    return "Needs Review", 1
