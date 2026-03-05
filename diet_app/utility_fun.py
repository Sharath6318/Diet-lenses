def daily_calorie_consumaption(height, weight, age, gender = "male", activity_leval = 1.2):

    bmr = 0

    if gender == "male":

        bmr = 10 * weight + 6.25 * height - 5 * age + 5

    else:

        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    calorie = bmr * activity_leval

    return round(calorie)

# print(daily_calorie_consumaption(165, 55, 32))

