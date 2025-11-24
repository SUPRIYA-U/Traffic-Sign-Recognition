from src.data_loader import get_data_generators
from src.train import train_model
from src.evaluate import evaluate_model
import os
from utils.utils import plot_history

DATA_DIR = 'data'
TRAIN_DIR = os.path.join(DATA_DIR, 'Train')
TEST_DIR = os.path.join(DATA_DIR, 'Test')
IMG_SIZE = (32, 32)
BATCH_SIZE = 32
EPOCHS = 10
MODEL_PATH = 'models/cnn_model.kerasx'

if __name__ == '__main__':
    train_gen, val_gen, test_gen = get_data_generators(TRAIN_DIR, TEST_DIR, IMG_SIZE, BATCH_SIZE)
    print("Train samples:", train_gen.samples)
    print("Validation samples:", val_gen.samples)
    print("Test samples:", test_gen.samples)
    num_classes = train_gen.num_classes

    model, history = train_model(train_gen, val_gen, input_shape=IMG_SIZE + (3,), num_classes=num_classes, epochs=EPOCHS)

    os.makedirs('models', exist_ok=True)
    model.save(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    plot_history(history)

    evaluate_model(model, test_gen)
