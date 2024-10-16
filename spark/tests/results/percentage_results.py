test_percentage_perfect_classes = {
    "data_quality": {
        "value": 0.9,
        "details": [
            {"feature_name": "num1", "score": 0.4},
            {"feature_name": "num2", "score": 0.0},
            {"feature_name": "cat1", "score": 0.0},
            {"feature_name": "cat2", "score": 0.0},
        ],
    },
    "model_quality": {"value": -1, "details": []},
    "drift": {"value": 1.0, "details": []},
}

test_percentage_easy_dataset = {
    "data_quality": {
        "value": 1.0,
        "details": [
            {"feature_name": "num1", "score": 0.0},
            {"feature_name": "num2", "score": 0.0},
            {"feature_name": "cat1", "score": 0.0},
            {"feature_name": "cat2", "score": 0.0},
        ],
    },
    "model_quality": {"value": -1, "details": []},
    "drift": {
        "value": 0.5,
        "details": [
            {"feature_name": "num1", "score": 1.0},
            {"feature_name": "num2", "score": 1.0},
        ],
    },
}

test_percentage_abalone = {
    "data_quality": {
        "value": 0.9926990038721882,
        "details": [
            {"feature_name": "Length", "score": 0.01223729715349827},
            {"feature_name": "Diameter", "score": 0.013833466347432828},
            {"feature_name": "Height", "score": 0.007182761372705506},
            {"feature_name": "Whole_weight", "score": 0.006916733173716414},
            {"feature_name": "Shucked_weight", "score": 0.011705240755520084},
            {"feature_name": "Viscera_weight", "score": 0.006118648576749135},
            {"feature_name": "Shell_weight", "score": 0.007714817770683693},
            {"feature_name": "Sex", "score": 0.0},
            {"feature_name": "pred_id", "score": 0.0},
        ],
    },
    "model_quality": {"value": 1.0, "details": []},
    "drift": {
        "value": 0.6666666666666667,
        "details": [
            {"feature_name": "pred_id", "score": 1.0},
            {"feature_name": "Diameter", "score": 1.0},
            {"feature_name": "Height", "score": 1.0},
        ],
    },
}
