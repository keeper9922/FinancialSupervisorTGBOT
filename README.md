To install all modules, that used in the project, you want to run:
`pip install -r requirements.txt` in terminal.
## How to configure bot?
It is very easy. You want to edit `.env` file. It's insides should look like this:
```
TOKEN=your_token
DATABASE=data.db
LANGUAGE=EN
LANGUAGE_FILE=language.json
```
**Only** field you want to really care about is the **TOKEN** field.
Also, you can choose here your preferred language (only completed `ru` and `en`).
You can easily add any language you want in `language.json`.
## How to run bot?
Run file `aiogram_run.py` and your bot is ready.