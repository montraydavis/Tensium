import string

import keras
import pandas as pd
import tensorflow as tf
import numpy as np

from Tensium.goals.TensiumBaseGoal import TensiumBaseGoal
from Tensium.envs.TensiumEnv import TensiumEnv

from tensorflow import feature_column
from keras.models import Sequential
from keras.layers import Dense, Dropout


class TestCaseModelCallback(keras.callbacks.Callback):
    required_accuracy: float

    def __init__(self, required_accuracy=.95) -> None:
        super().__init__()
        self.required_accuracy = required_accuracy

    def on_epoch_end(self, epoch, logs=None):
        if logs is not None and logs.get('accuracy') >= self.required_accuracy:
            self.model.stop_training = True


class TestCase():
    id: string
    possible_actions: list
    goal: TensiumBaseGoal

    def _create_model(self, feature_layer, optimizer, loss):
        model = Sequential([
            feature_layer,
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(64, activation='relu'),
            Dense(1, activation='sigmoid')
        ])

        model.compile(optimizer=optimizer,
                      loss=loss,
                      metrics=['accuracy'])

        return model

    def _create_sub_set(self, action_history: list, labels: list):
        frames = []
        for i in action_history:
            _df = pd.DataFrame(np.array(i).reshape(-1, 4), columns=labels)
            frames.append(_df)

        df = pd.concat(frames)
        labels_ds = df.pop(labels[-1])
        df = tf.data.Dataset.from_tensor_slices((dict(df), labels_ds))
        df = df.batch(1)

        return df

    def _create_set(self, action_history: list, labels: list):
        df = pd.DataFrame([i for i in action_history], columns=labels)
        labels_ds = df.pop(labels[-1])
        df = tf.data.Dataset.from_tensor_slices((dict(df), labels_ds))
        df = df.batch(1)

        return df

    def __init__(self, id: string, possible_actions: list, goal: TensiumBaseGoal, working_dir: string, reset_callback=None) -> None:
        self.id = id
        self.possible_actions = possible_actions
        self.goal = goal
        self.working_dir = working_dir
        self.reset_callback = reset_callback

        self.env = TensiumEnv(possible_actions, goal, working_dir,
                              reset_callback)

    def Learn(self, n_steps=10000, epochs=15, optimizer='adam', loss='mean_squared_error', force_end_success=0, required_accuracy=.95):

        for i in range(n_steps):
            if force_end_success > 0:
                successful_sequences = len(
                    [i for i in self.env.action_history if i[-1] == 1])

                if successful_sequences >= force_end_success:
                    break

            sample = self.env.action_space.sample()
            self.env.step(sample)
            self.env.reset()

            self.action_history = self.env.action_history

        labels = ["LABEL_" + str(i)
                  for i in range(len(self.env.action_history[0]))]

        train_ds = self._create_set(
            [i for i in self.env.action_history], labels)

        feature_columns = [
            feature_column.numeric_column(i) for i in labels[:-1]]
        feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

        model = self._create_model(feature_layer, optimizer, loss)
        model.fit(train_ds, epochs=epochs, callbacks=[
                  TestCaseModelCallback(required_accuracy=required_accuracy)])
        model.save(self.working_dir+'\\train\\'+self.id)

    def Run(self, n_steps=500):
        model = keras.models.load_model(
            self.working_dir+'\\train\\'+self.id)

        for i in range(n_steps):
            self.env.reset()
            action_history = [i for i in self.env.action_history]
            action_history_labels = ["LABEL_" + str(i)
                                     for i in range(len(self.env.action_history[0]))]

            train_ds = self._create_sub_set(
                action_history, action_history_labels)

            prediction = model.predict(train_ds)
            best_sequence = np.argmax(prediction)
            best_sequence = action_history[best_sequence]
            self.env.step(best_sequence[:-1])

    def Finish(self):
        self.env.driver_wrapper.driver.quit()
