import openai

def parse_cv(cv_text, openai_api_key, max_tokens=1000):
    openai.api_key = openai_api_key

    # Define the conversation with the CV text as a variable
    conversation = [
        {"role": "system", "content": "Vous êtes un assistant d'analyse de CV."},
        {"role": "user", "content": f"Analysez le CV suivant et extrayez les informations pertinentes :\n\n{cv_text}"},
        {"role": "assistant", "content": "Informations extraites en JSON avec exactement la structure suivante : {information_basique : {nom, prenom, email, numero_telephone, location, linkedin_url, nom_universite, niveau_education, titre_professionnel}, Expérience_professionnelle : [{Poste, Entreprise, Durée(format : { 'start_date' : %m-YYYY, 'end_date' : %m-YYYY} ), Responsabilités/Réalisations}], skills : {Programming_languages}}"},  
    ]

    # Make the API call
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=conversation,
    max_tokens=max_tokens, 
    temperature=0
    )

    # Extract the assistant's reply
    assistant_reply = response['choices'][0]['message']['content']

    # Print or use the assistant's reply as needed
    return assistant_reply



