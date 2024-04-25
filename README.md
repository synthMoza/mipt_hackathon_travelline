# TravelLine chat assistant
This is a solution for the case presented by TravelLine company. The problem is to create a bot which will replace humans and answer users' questions based on the database of knowledge.

## Idea
Our idea utilizes RAG algorithm. We use pre-trained LLM models to answer the question by consturction the prompt with the related document from the database. To find the appropriate document, we have the pre-calculated database of documents embeddings. By obtaining user's query embeddings and calculating cosine simularity, we can find the most releant documents. We use GigaChat API for generating the answer, and SBert model from hugging face to get embeddings.

## Requirements
Before running the project, you must obtain GigaChat credentials. You may find the instruction how to do so [here](https://developers.sber.ru/docs/ru/gigachat/individuals-quickstart).

## How To Run
To run chat assistant:
1. Make sure you have `python3.12` and `python3.12-venv`  installed on your machine. Other python versions may be supported, but no guarantees.
2. Clone the repository
  `git clone https://github.com/synthMoza/mipt_hackathon_travelline.git`
3. Install dependencies:
  ```bash
  python3.12 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
4. Create `config.json` file and fill it with paths to configs and GigaChat credentials:
   ```json
   {
       "credentials": "<your-gigachat-credentials>",
       "thought_config": "<path_to_repo>/src/travelline/backend/llm/gigathought.yaml",
       "detailizer_config": "<path_to_repo>/src/travelline/backend/llm/gigadetailizer.yaml"
   }
   ```
5. Run server and navigate to http://127.0.0.1 to start chatting:
```
python3 src/travelline/web/travelline_ai_support/manage.py
```

## Authors
Students of 1st year Master's degree in MIPT DREC facility
- Alexey Eganyan (synthMoza)
- Eugene Zorin (Greezzee)
- Stanislav Sidelnikov (sin-diesel)
- Vasilii Zaitsev (ZVasilii)
- Vladislav Loznovenko (Vlad-creator)

March-April 2024

