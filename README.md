# TravelLine chat assistant
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
       "credentials": "",
       "thought_config": "<path_to_repo>/src/travelline/backend/llm/gigathought.yaml",
       "detailizer_config": "<path_to_repo>/src/travelline/backend/llm/gigadetailizer.yaml"
   }
   ```
5. Run server and navigate to http://127.0.0.1 to start chatting:
```
python3 src/travelline/web/travelline_ai_support/manage.py
```
