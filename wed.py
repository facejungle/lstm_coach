
import importlib


# Список классов для импорта
classes_to_import = [
    {"module": "app.shared.exchanges.binance", "class": "Binance"},
]
for class_info in classes_to_import:
    module = importlib.import_module(class_info["module"])
    class_ = getattr(module, class_info["class"])
    instance = class_()
    instance.parse_instruments()
