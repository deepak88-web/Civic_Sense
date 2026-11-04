
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dropout, Dense


def build_lstm_model(
    embedding_matrix,
    num_classes,
    max_sequence_length,
    lstm_units=64,
    dropout_rate=0.3,
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    embedding_trainable=True,
    mask_zero=True,
    output_activation="softmax"
):
    """
    Build the LSTM classification model using
    pretrained Word2Vec embeddings.
    """

    vocab_size = embedding_matrix.shape[0]
    embedding_dim = embedding_matrix.shape[1]

    model = Sequential([
        Embedding(
            input_dim=vocab_size,
            output_dim=embedding_dim,
            weights=[embedding_matrix],
            mask_zero=mask_zero,
            trainable=embedding_trainable
        ),

        LSTM(lstm_units),

        Dropout(dropout_rate),

        Dense(num_classes, activation=output_activation)
    ])

    model.compile(
        optimizer=optimizer,
        loss=loss,
        metrics=["accuracy"]
    )

    model.build(
        input_shape=(None, max_sequence_length)
    )

    return model
