def calculate_experience_relevance_adjusted(months_experience_profile, months_experience_job, divisor=4):
    '''
        abs(months_experience_profile - months_experience_job): This calculates the absolute difference between the candidate's months of experience (months_experience_profile) and the required months of experience for the job (months_experience_job).

        1 - abs(months_experience_profile - months_experience_job) / 5: This part calculates a score based on the difference, where a smaller difference results in a higher score. The division by 5 is a scaling factor, and you can adjust it based on the range of your experience data.
    '''

    # divisor: more the divisor is low more the months_experience_profile have more importance

    # ask the business to select this divisor

    years_experience_profile =  months_experience_profile / 12
    years_experience_job = months_experience_job / 12
    return max(0, 1 - abs(years_experience_profile - years_experience_job) / divisor)


def matching(cv, job):

    score = 0

    score_experience = calculate_experience_relevance_adjusted(cv['months_experiences'], job['months_experiences'])

    return score