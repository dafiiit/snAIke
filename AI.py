# Importiere die Funktion aus modul1
# from snake_game_basic import meine_funktion
import numpy as np


class AI:
    def __init__(
        self,
        input_size=20 * 20,
        hidden1_size=64,
        hidden2_size=32,
        hidden3_size=16,
        output_size=3,
        weights_file_prefix="neural_net_weights"
    ):
        # Gewichtsmatrizen und Bias initialisieren
        np.random.seed(42)
        self.weights_input_hidden1 = np.random.rand(input_size, hidden1_size)
        self.weights_hidden1_hidden2 = np.random.rand(hidden1_size, hidden2_size)
        self.weights_hidden2_hidden3 = np.random.rand(hidden2_size, hidden3_size)
        self.weights_hidden3_output = np.random.rand(hidden3_size, output_size)

        self.bias_hidden1 = np.zeros((1, hidden1_size))
        self.bias_hidden2 = np.zeros((1, hidden2_size))
        self.bias_hidden3 = np.zeros((1, hidden3_size))
        self.bias_output = np.zeros((1, output_size))
        
        # Versuche, die Gewichtsmatrizen und Bias-Werte zu laden
        try:
            self.load_weights_bias(weights_file_prefix)
            print("Gewichtsmatrizen und Bias-Werte erfolgreich geladen.")
        except FileNotFoundError:
            print("Keine gespeicherten Gewichtsmatrizen und Bias-Werte gefunden.")

    def save_weights_bias(self, file_prefix="neural_net_weights"):
        # Speichere die Gewichtsmatrizen und Bias-Werte in separate Dateien
        np.save(file_prefix + "_input_hidden1.npy", self.weights_input_hidden1)
        np.save(file_prefix + "_hidden1_hidden2.npy", self.weights_hidden1_hidden2)
        np.save(file_prefix + "_hidden2_hidden3.npy", self.weights_hidden2_hidden3)
        np.save(file_prefix + "_hidden3_output.npy", self.weights_hidden3_output)

        np.save(file_prefix + "_bias_hidden1.npy", self.bias_hidden1)
        np.save(file_prefix + "_bias_hidden2.npy", self.bias_hidden2)
        np.save(file_prefix + "_bias_hidden3.npy", self.bias_hidden3)
        np.save(file_prefix + "_bias_output.npy", self.bias_output)

    def load_weights_bias(self, file_prefix="neural_net_weights"):
        # Lade die Gewichtsmatrizen und Bias-Werte aus den gespeicherten Dateien
        self.weights_input_hidden1 = np.load(file_prefix + "_input_hidden1.npy")
        self.weights_hidden1_hidden2 = np.load(file_prefix + "_hidden1_hidden2.npy")
        self.weights_hidden2_hidden3 = np.load(file_prefix + "_hidden2_hidden3.npy")
        self.weights_hidden3_output = np.load(file_prefix + "_hidden3_output.npy")

        self.bias_hidden1 = np.load(file_prefix + "_bias_hidden1.npy")
        self.bias_hidden2 = np.load(file_prefix + "_bias_hidden2.npy")
        self.bias_hidden3 = np.load(file_prefix + "_bias_hidden3.npy")
        self.bias_output = np.load(file_prefix + "_bias_output.npy")

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def relu(self, x):
        return np.maximum(0, x)

    def relu_derivative(self, x):
        return np.where(x > 0, 1, 0)

    def train(self, input_data, output_data, reward= 0, learning_rate=0.01, epochs=1000):  # epochs auf 10000 setzen
        for epoch in range(epochs):
            # Forward Propagation
            hidden1_output = self.relu(
                np.dot(input_data, self.weights_input_hidden1) + self.bias_hidden1
            )
            hidden2_output = self.relu(
                np.dot(hidden1_output, self.weights_hidden1_hidden2) + self.bias_hidden2
            )
            hidden3_output = self.relu(
                np.dot(hidden2_output, self.weights_hidden2_hidden3) + self.bias_hidden3
            )
            model_output = self.sigmoid(
                np.dot(hidden3_output, self.weights_hidden3_output) + self.bias_output
            )

            # Fehlergradienten berechnen
            error = output_data - model_output
            d_output = error * self.sigmoid_derivative(model_output)

            # Backpropagation
            error_hidden3 = d_output.dot(self.weights_hidden3_output.T)
            d_hidden3 = error_hidden3 * self.relu_derivative(hidden3_output)

            error_hidden2 = d_hidden3.dot(self.weights_hidden2_hidden3.T)
            d_hidden2 = error_hidden2 * self.relu_derivative(hidden2_output)

            error_hidden1 = d_hidden2.dot(self.weights_hidden1_hidden2.T)
            d_hidden1 = error_hidden1 * self.relu_derivative(hidden1_output)

            # Gewichtsmatrizen und Bias aktualisieren
            self.weights_hidden3_output += (
                hidden3_output.T.dot(d_output) * learning_rate
            )
            self.bias_output += np.sum(d_output, axis=0, keepdims=True) * learning_rate

            self.weights_hidden2_hidden3 += (
                hidden2_output.T.dot(d_hidden3) * learning_rate
            )
            self.bias_hidden3 += (
                np.sum(d_hidden3, axis=0, keepdims=True) * learning_rate
            )

            self.weights_hidden1_hidden2 += (
                hidden1_output.T.dot(d_hidden2) * learning_rate
            )
            self.bias_hidden2 += (
                np.sum(d_hidden2, axis=0, keepdims=True) * learning_rate
            )

            self.weights_input_hidden1 += input_data.T.dot(d_hidden1) * learning_rate
            self.bias_hidden1 += (
                np.sum(d_hidden1, axis=0, keepdims=True) * learning_rate
            )
            
            # Nach dem Training die Gewichtsmatrizen und Bias-Werte speichern
            self.save_weights_bias()

    def predict(self, input_data, threshold=0.5):
        hidden1_output = self.relu(
            np.dot(input_data, self.weights_input_hidden1) + self.bias_hidden1
        )
        hidden2_output = self.relu(
            np.dot(hidden1_output, self.weights_hidden1_hidden2) + self.bias_hidden2
        )
        hidden3_output = self.relu(
            np.dot(hidden2_output, self.weights_hidden2_hidden3) + self.bias_hidden3
        )
        model_output = self.sigmoid(
            np.dot(hidden3_output, self.weights_hidden3_output) + self.bias_output
        )
        # dafür sorgen, dass nur ein Wert 1 ist
        max_index=0
        output_vektor=model_output[0]
        print("model_output: ", output_vektor)

        for i in range(len(output_vektor)):
            if output_vektor[i]> output_vektor[max_index]:
                max_index=i
        binary_output = np.zeros(len(output_vektor))
        binary_output[max_index]=1
        print("binary_output: ", binary_output)
        
        return binary_output

