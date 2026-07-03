"""
skills_db.py
Curated list of technical skills used for keyword-based extraction from
resumes and job descriptions. Organized by category purely for readability
-- extraction treats them as one flat, lower-cased set.

Feel free to extend this list for other domains (e.g., marketing, finance).
"""

SKILLS_DB = {
    "Programming Languages": [
        "python", "java", "c++", "c", "c#", "javascript", "typescript", "go",
        "golang", "rust", "r", "matlab", "scala", "kotlin", "swift", "php",
        "sql", "bash", "shell scripting", "html", "css",
    ],
    "ML / AI / Data Science": [
        "machine learning", "deep learning", "neural networks", "cnn",
        "rnn", "lstm", "transformer", "nlp", "natural language processing",
        "computer vision", "opencv", "reinforcement learning",
        "generative ai", "llm", "large language models", "rag",
        "retrieval augmented generation", "prompt engineering",
        "fine-tuning", "lora", "peft", "huggingface", "transformers",
        "pytorch", "tensorflow", "keras", "scikit-learn", "sklearn",
        "pandas", "numpy", "matplotlib", "seaborn", "xgboost", "lightgbm",
        "opencv", "yolo", "langchain", "llamaindex", "vector database",
        "faiss", "chromadb", "pinecone", "openai api", "spacy", "nltk",
        "data preprocessing", "feature engineering", "model evaluation",
        "mlops", "mlflow", "data visualization", "statistics",
        "time series", "recommendation systems", "gans",
    ],
    "Web / Backend Development": [
        "flask", "django", "fastapi", "node.js", "express.js", "react",
        "react.js", "angular", "vue.js", "next.js", "rest api", "restful",
        "graphql", "microservices", "api development", "websockets",
        "spring boot", "asp.net",
    ],
    "Databases": [
        "mysql", "postgresql", "mongodb", "sqlite", "redis", "oracle",
        "firebase", "cassandra", "dynamodb", "elasticsearch",
    ],
    "Cloud / DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "ci/cd", "jenkins", "git", "github", "gitlab", "terraform",
        "linux", "nginx", "azure ai", "aws bedrock", "vertex ai",
        "watsonx", "ibm watsonx", "cloud computing", "serverless",
    ],
    "Tools / Other": [
        "jira", "agile", "scrum", "postman", "vs code", "jupyter",
        "tableau", "power bi", "excel", "data structures",
        "algorithms", "system design", "oop", "object oriented programming",
        "unit testing", "debugging", "problem solving",
    ],
}

# Flat, lower-cased list used for matching
ALL_SKILLS = sorted({s.lower() for group in SKILLS_DB.values() for s in group})
