def calculate_experience_relevance_adjusted(years_experience_profile, years_experience_job, divisor=4):
    '''
        abs(years_experience_profile - years_experience_job): This calculates the absolute difference between the candidate's years of experience (years_experience_profile) and the required years of experience for the job (years_experience_job).

        1 - abs(years_experience_profile - years_experience_job) / 5: This part calculates a score based on the difference, where a smaller difference results in a higher score. The division by 5 is a scaling factor, and you can adjust it based on the range of your experience data.
    '''

    # divisor: more the divisor is low more the years_experience_profile have more importante


    # ask the business to select this divisor


    return max(0, 1 - abs(years_experience_profile - years_experience_job) / divisor)