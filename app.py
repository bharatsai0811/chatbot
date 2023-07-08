from flask import Flask, render_template, request
import wikipediaapi
from transformers import pipeline

app = Flask(__name__)

def search_wikipedia(topic):
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent='My Wikipedia Search App/1.0'
    )

    page = wiki_wiki.page(topic)

    if page.exists():
        content = page.text
        return content
    else:
        return None

def answer_question(question, content):  
    model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
    qa_pipeline = pipeline("question-answering", model=model_name)
    answer = qa_pipeline(question=question, context=content)
    return answer["answer"]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        topic = request.form['topic']
        print(topic)
        page_content = search_wikipedia(topic)

        if page_content:
            return render_template('index.html', topic=topic, content=page_content)
        else:
            return render_template('index.html', error=True)

    return render_template('index.html')

@app.route('/answer', methods=['POST'])
def get_answer():
    question = request.form['question']
    content = request.form['content']
    topic = request.form['topic']
    answer = answer_question(question, content)
    return render_template('index.html', topic=topic, content=content, question=question, answer=answer)
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
