import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    url = "./adult.data.csv"
    df = pd.read_csv(url)
    df.columns = [column.replace(" ", "_") for column in df.columns]

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df["race"].value_counts()

    # What is the average age of men?
    average_age_men = round(df.query('sex=="Male"')["age"].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    peopleWithBachelorsDeg = df.query('education == "Bachelors"')["education"].count()
    totalRows = df.shape[0]
    percentage_bachelors = (peopleWithBachelorsDeg / totalRows) * 100
    percentage_bachelors = float("{:.1f}".format(percentage_bachelors))

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education: pd.DataFrame = df[
        df["education"].isin(["Bachelors", "Masters", "Doctorate"])
    ]
    higher_education_count = higher_education["salary"].count()
    higher_education_with_more_sal_count = higher_education.query('salary == ">50K"')[
        "salary"
    ].count()

    lower_education: pd.DataFrame = df[
        ~df["education"].isin(["Bachelors", "Masters", "Doctorate"])
    ]
    lower_education_count = lower_education["salary"].count()
    lower_education_with_more_sal_count = lower_education.query('salary == ">50K"')[
        "salary"
    ].count()

    # percentage with salary >50K
    higher_education_rich = round(
        (higher_education_with_more_sal_count / higher_education_count) * 100, 1
    )
    lower_education_rich = round(
        (lower_education_with_more_sal_count / lower_education_count) * 100, 1
    )

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers: pd.DataFrame = df[df["hours-per-week"].isin([min_work_hours])]

    num_min_workers_count = num_min_workers["salary"].count()
    min_work_hours_with_more_sal_count = num_min_workers.query('salary == ">50K"')[
        "salary"
    ].count()

    rich_percentage = round(
        (min_work_hours_with_more_sal_count / num_min_workers_count) * 100, 1
    )

    # What country has the highest percentage of people that earn >50K?
    countries = df.dropna()["native-country"].unique()
    highest_earners_total_in_countries = pd.Series(dtype=object)
    per_of_highest_earners_in_countries = pd.Series(dtype=object)

    for i in countries:
        country = df[df["native-country"] == i]
        highest_earners_in_country = country[country["salary"] == ">50K"]

        country_totals = pd.Series(country["native-country"]).value_counts()
        highest_earners_in_country_totals = pd.Series(
            highest_earners_in_country["native-country"]
        ).value_counts()

        per_of_highest_earners_in_country = round(
            (highest_earners_in_country_totals / country_totals) * 100, 1
        )

        highest_earners_total_in_countries = pd.concat(
            [highest_earners_total_in_countries, country_totals]
        )
        per_of_highest_earners_in_countries = pd.concat(
            [per_of_highest_earners_in_countries, per_of_highest_earners_in_country]
        )

    per_of_highest_earners_in_countries = (
        per_of_highest_earners_in_countries.dropna().sort_values()
    )
    highest_earning_country = per_of_highest_earners_in_countries.last_valid_index()
    highest_earning_country_percentage = per_of_highest_earners_in_countries[
        highest_earning_country
    ]

    # Identify the most popular occupation for those who earn >50K in India.
    highest_earners_india = df.loc[
        (df["salary"] == ">50K") & (df["native-country"] == "India")
    ]
    highest_earners_india_occupations = highest_earners_india[
        "occupation"
    ].value_counts()
    top_IN_occupation = (
        highest_earners_india_occupations.sort_values().last_valid_index()
    )

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(
            f"Percentage with higher education that earn >50K: {higher_education_rich}%"
        )
        print(
            f"Percentage without higher education that earn >50K: {lower_education_rich}%"
        )
        print(f"Min work time: {min_work_hours} hours/week")
        print(
            f"Percentage of rich among those who work fewest hours: {rich_percentage}%"
        )
        print("Country with highest percentage of rich:", highest_earning_country)
        print(
            f"Highest percentage of rich people in country: {highest_earning_country_percentage}%"
        )
        print("Top occupations in India:", top_IN_occupation)

    return {
        "race_count": race_count,
        "average_age_men": average_age_men,
        "percentage_bachelors": percentage_bachelors,
        "higher_education_rich": higher_education_rich,
        "lower_education_rich": lower_education_rich,
        "min_work_hours": min_work_hours,
        "rich_percentage": rich_percentage,
        "highest_earning_country": highest_earning_country,
        "highest_earning_country_percentage": highest_earning_country_percentage,
        "top_IN_occupation": top_IN_occupation,
    }
