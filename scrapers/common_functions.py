def calculate_score(created_date, closed_date, area, population):
    duration_in_seconds = float((closed_date - created_date).total_seconds())
    population_density = float(population)/float(area)
    return (duration_in_seconds/population_density) / 1e9
