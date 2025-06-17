def classify_meal(cal, protein, fat, carbs):
    total_kcal = protein * 4 + fat * 9 + carbs * 4
    if abs(total_kcal - cal) > 100:
        return "Inconsistent data"

    prot_ratio = (protein * 4) / total_kcal
    fat_ratio = (fat * 9) / total_kcal
    carb_ratio = (carbs * 4) / total_kcal

    def check_range(val, healthy, neutral):
        if healthy[0] <= val <= healthy[1]:
            return "healthy"
        elif neutral[0] <= val <= neutral[1]:
            return "neutral"
        else:
            return "unhealthy"

    cal_status = check_range(cal, (400, 800), (800, 1000))
    prot_status = check_range(prot_ratio, (0.15, 0.30), (0.10, 0.15))
    fat_status = check_range(fat_ratio, (0.20, 0.30), (0.30, 0.40))
    carb_status = check_range(carb_ratio, (0.45, 0.60), (0.35, 0.45))

    statuses = [cal_status, prot_status, fat_status, carb_status]
    unhealthy_count = statuses.count("unhealthy")
    healthy_count = statuses.count("healthy")

    classification_scores = ["Very Unhealthy", "Unhealthy", "Neutral", "Healthy", "Very Healthy"]

    return classification_scores[healthy_count]

def classify_meal_with_scale(cal, protein, fat, carbs):
    total_kcal = protein * 4 + fat * 9 + carbs * 4
    if abs(total_kcal - cal) > 100:
        return "Inconsistent data", 0

    prot_ratio = (protein * 4) / total_kcal
    fat_ratio = (fat * 9) / total_kcal
    carb_ratio = (carbs * 4) / total_kcal

    def check_range(val, ranges):
        for i, (low, high) in enumerate(ranges):
            if low <= val <= high:
                return i
        return len(ranges) - 1

    cal_scale = check_range(cal, [(400, 600), (600, 800), (800, 1000), (1000, 1200), (1200, float('inf'))])
    prot_scale = check_range(prot_ratio, [(0.15, 0.20), (0.20, 0.30), (0.10, 0.15), (0.05, 0.10), (0, 0.05)])
    fat_scale = check_range(fat_ratio, [(0.20, 0.25), (0.25, 0.30), (0.30, 0.40), (0.40, 0.50), (0.50, float('inf'))])
    carb_scale = check_range(carb_ratio, [(0.45, 0.50), (0.50, 0.60), (0.35, 0.45), (0.25, 0.35), (0, 0.25)])

    avg_scale = round((cal_scale + prot_scale + fat_scale + carb_scale) / 4)

    classification = ["Very Healthy", "Healthy", "Neutral", "Unhealthy", "Very Unhealthy"]
    return classification[avg_scale], avg_scale

def classify_meal_with_scale_v2(cal, protein, fat, carbs):
    total_kcal = protein * 4 + fat * 9 + carbs * 4
    if abs(total_kcal - cal) > 100:
        return "Inconsistent data", 0

    prot_ratio = (protein * 4) / total_kcal
    fat_ratio = (fat * 9) / total_kcal
    carb_ratio = (carbs * 4) / total_kcal

    def check_range(val, ranges):
        for i, (low, high) in enumerate(ranges):
            if low <= val <= high:
                return i
        return len(ranges) - 1

    cal_scale = check_range(cal, [(-4, -2), (-2, 0), (0, 2), (2, 4)])
    prot_scale = check_range(prot_ratio, [(-4, -2), (-2, 0), (0, 2), (2, 4)])
    fat_scale = check_range(fat_ratio, [(-4, -2), (-2, 0), (0, 2), (2, 4)])
    carb_scale = check_range(carb_ratio, [(-4, -2), (-2, 0), (0, 2), (2, 4)])

    avg_scale = round((cal_scale + prot_scale + fat_scale + carb_scale) / 4)

    classification = ["Very Unhealthy", "Unhealthy", "Neutral", "Healthy", "Very Healthy"]
    return classification[avg_scale], avg_scale

def classify_meal_with_scale_v3(cal, protein, fat, carbs):
    total_kcal = protein * 4 + fat * 9 + carbs * 4
    if abs(total_kcal - cal) > 100:
        return "Inconsistent data", 0

    # Calculate ratios
    prot_ratio = (protein * 4) / total_kcal
    fat_ratio = (fat * 9) / total_kcal
    carb_ratio = (carbs * 4) / total_kcal

    # Define ranges for healthiness
    def check_healthiness(value, healthy_range, neutral_range):
        if healthy_range[0] <= value <= healthy_range[1]:
            return 1  # Healthy
        elif neutral_range[0] <= value <= neutral_range[1]:
            return 0  # Neutral
        else:
            return -1  # Unhealthy

    # Healthiness checks
    cal_score = check_healthiness(cal, (400, 800), (800, 1200))
    prot_score = check_healthiness(prot_ratio, (0.15, 0.30), (0.10, 0.15))
    fat_score = check_healthiness(fat_ratio, (0.20, 0.35), (0.35, 0.40))
    carb_score = check_healthiness(carb_ratio, (0.45, 0.65), (0.35, 0.45))

    # Calculate total score
    total_score = cal_score + prot_score + fat_score + carb_score

    # Classification based on total score
    classification = ["Very Unhealthy", "Unhealthy", "Neutral", "Healthy", "Very Healthy"]
    return classification[max(0, min(total_score, 4))], total_score

def classify_meal_with_notes(cal, protein, fat, carbs):
    total_kcal = protein * 4 + fat * 9 + carbs * 4
    if abs(total_kcal - cal) > 100:
        return "Inconsistent data", 0, "The calculated total calories do not match the provided value."

    # Calculate ratios
    prot_ratio = (protein * 4) / total_kcal
    fat_ratio = (fat * 9) / total_kcal
    carb_ratio = (carbs * 4) / total_kcal

    # Define ranges for healthiness
    def check_healthiness(value, healthy_range, neutral_range):
        if healthy_range[0] <= value <= healthy_range[1]:
            return 1, "Sufficient amount, within healthy range."
        elif neutral_range[0] <= value <= neutral_range[1]:
            return 0, "Average amount, within neutral range."
        else:
            return -1, "Unhealthy"

    # Healthiness checks with notes
    cal_score, cal_note = check_healthiness(cal, (400, 800), (800, 1200))
    prot_score, prot_note = check_healthiness(prot_ratio, (0.15, 0.30), (0.10, 0.15))
    fat_score, fat_note = check_healthiness(fat_ratio, (0.20, 0.35), (0.35, 0.40))
    carb_score, carb_note = check_healthiness(carb_ratio, (0.45, 0.65), (0.35, 0.45))

    # Generate notes for all scenarios
    notes = []
    if cal_score == -1:
        if cal < 400:
            notes.append("Calories are too low. Consider adding more nutrient-dense foods.")
        elif cal > 1200:
            notes.append("Calories are too high. Consider reducing portion sizes.")
    elif cal_score == 0:
        notes.append("Calories are within an average range.")
    elif cal_score == 1:
        notes.append("Calories are within a healthy range.")

    if prot_score == -1:
        notes.append("Protein content is insufficient. Consider adding protein-rich foods like chicken or beans.")
    elif prot_score == 0:
        notes.append("Protein content is average, within neutral range.")
    elif prot_score == 1:
        notes.append("Protein content is sufficient, within healthy range.")

    if fat_score == -1:
        notes.append("Fat content is too high. Consider reducing fatty foods or using healthier fats.")
    elif fat_score == 0:
        notes.append("Fat content is average, within neutral range.")
    elif fat_score == 1:
        notes.append("Fat content is sufficient, within healthy range.")

    if carb_score == -1:
        notes.append("Carbohydrate content is insufficient. Consider adding energy-rich foods like rice or bread.")
    elif carb_score == 0:
        notes.append("Carbohydrate content is average, within neutral range.")
    elif carb_score == 1:
        notes.append("Carbohydrate content is sufficient, within healthy range.")

    # Calculate total score
    total_score = cal_score + prot_score + fat_score + carb_score

    # Classification based on total score
    classification = ["Very Unhealthy", "Unhealthy", "Neutral", "Healthy", "Very Healthy"]
    return classification[max(0, min(total_score, 4))], total_score, " ".join(notes)
