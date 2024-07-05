from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def preprocess(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation, numbers, etc. if necessary
    return text

@app.route('/compare', methods=['POST'])
def compare_documents():
    try:
        # Get the uploaded files
        doc1_file = request.files['document1']
        doc2_file = request.files['document2']
        
        # Read the contents of the files
        doc1 = doc1_file.read().decode('utf-8')
        doc2 = doc2_file.read().decode('utf-8')
        
        # Preprocess the documents
        doc1 = preprocess(doc1)
        doc2 = preprocess(doc2)
        
        # Create a list of documents
        documents = [doc1, doc2]
        
        # Convert the text data into TF-IDF features
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        # Compute cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        
        # Get the similarity percentage
        similarity_percentage = cosine_sim[0][0] * 100
        
        # Return the similarity percentage as JSON response
        return jsonify({
            'similarity_percentage': similarity_percentage
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
