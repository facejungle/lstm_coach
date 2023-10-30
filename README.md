# RNN LSTM AI Coach

pyinstaller --onefile --noconsole --clean --icon='coach\app\res\icon.ico' --add-data "lstm_coach\res:app\res" --add-data "lstm_coach\config.json:shared\exchanges" -n lstm-coach "lstm_coach\main.py"
