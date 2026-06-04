def predict_message(model, msg):

    length = len(msg)
    words = len(msg.split())
    digits = sum(c.isdigit() for c in msg)
    upper = sum(c.isupper() for c in msg)

    free = 1 if "free" in msg.lower() else 0
    win = 1 if "win" in msg.lower() else 0
    click = 1 if "click" in msg.lower() else 0

    features = [[length, words, digits, upper, free, win, click]]

    return model.predict(features)[0]