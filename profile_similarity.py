import spacy
import spacy.cli
# Load the spaCy model with pre-trained Word2Vec embeddings

try:
    nlp = spacy.load("en_core_web_sm")
except:
    spacy.cli.download("en_core_web_sm")

nlp = spacy.load("en_core_web_sm")

def calculate_role_similarity(candidate_role, job_description_role):
    try:
        # Get the similarity score based on word embeddings
        candidate_role_embedding = nlp(candidate_role.lower()).vector
        job_description_role_embedding = nlp(job_description_role.lower()).vector

        # Calculate cosine similarity between the embeddings
        similarity_score = candidate_role_embedding.dot(job_description_role_embedding) / (
            (candidate_role_embedding**2).sum()**0.5 * (job_description_role_embedding**2).sum()**0.5
        )
        return similarity_score
    except KeyError:
        # Handle the case where one or both job titles are not in the vocabulary
        return 0

# Example usage
candidate_role = "mid-level data scientist"
job_description_role = "senior data scientist"

matching_score = calculate_role_similarity(candidate_role, job_description_role)
print(f"Matching Score: {matching_score}")
