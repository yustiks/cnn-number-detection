import time
import constants
from Trainer.Models.model_gnet_light import ModelGNetLight
from Trainer.Models.model_gnet_light_v2 import ModelGNetLightV2
from Trainer.Models.model_gnet_deep import ModelGNetDeep
from Trainer.Models.model_gnet_deep_v2 import ModelGNetDeepV2
from Trainer.Models.model_gnet_deep_v3 import ModelGNetDeepV3
from Trainer.Models.model_gnet_deep_deep import ModelGNetDeepDeep
from Trainer.Models.model import Model
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Activation, Flatten
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D


def main():
    model = ModelGNetLight('ultimate-data-15-epochs-128-batch-size')
    model.create_model()
    model.train_model_with_generator()
    model.save_model(visualize_model=True)
    #
    # model = ModelGNetLightV2('ultimate-data-15-epochs-128-batch-size')
    # model.create_model()
    # model.train_model()
    # model.save_model()

    # model = ModelGNetDeep('ultimate-data-15-epochs-128-batch-size')
    # model.create_model()
    # model.train_model()
    # model.save_model(visualize_model=True)
    #
    # model = ModelGNetDeepV2('ultimate-data-15-epochs-128-batch-size')
    # model.create_model()
    # model.train_model()
    # model.save_model(visualize_model=True)
    #
    # model = ModelGNetDeepV3('ultimate-data-15-epochs-128-batch-size')
    # model.create_model()
    # model.train_model()
    # model.save_model(visualize_model=True)
    #
    # model = ModelGNetDeepDeep('ultimate-data-15-epochs-128-batch-size')
    # model.create_model()
    # model.train_model()
    # model.save_model(visualize_model=True)

    # train multiple models for finding the perfect hyperparameters
    # train_multiple_models('full-dataset-aug-rand',
    #                       dense_layers=[0, 1, 2],
    #                       layer_sizes=[16, 32, 64],
    #                       conv_layers=[1, 2, 3])


def train_multiple_models(name_postfix, dense_layers=[0, 1, 2], layer_sizes=[16, 32, 64], conv_layers=[1, 2, 3]):
    for dense_layer in dense_layers:
        for layer_size in layer_sizes:
            for conv_layer in conv_layers:
                # give the model a name to create it again
                model_name = "{}-conv-{}-nodes-{}-dense-{}-{}".format(conv_layer, layer_size, dense_layer,
                                                                      int(time.time()), name_postfix)
                # create an instance of model
                model_obj = Model(model_name)

                # create model
                model_obj.model = Sequential()

                # add model layers
                model_obj.model.add(Conv2D(layer_size,
                                           kernel_size=3,
                                           input_shape=(constants.IMG_SIZE, constants.IMG_SIZE, constants.DIMENSION)))
                model_obj.model.add(Activation('relu'))
                model_obj.model.add(MaxPooling2D(pool_size=(2, 2)))

                for _ in range(conv_layer - 1):
                    model_obj.model.add(Conv2D(layer_size, kernel_size=3))
                    model_obj.model.add(Activation('relu'))
                    model_obj.model.add(MaxPooling2D(pool_size=(2, 2)))

                model_obj.model.add(Flatten())

                for _ in range(dense_layer):
                    model_obj.model.add(Dense(layer_size))
                    model_obj.model.add(Activation('relu'))

                model_obj.model.add(Dense(len(constants.CATEGORIES)))
                model_obj.model.add(Activation('softmax'))

                model_obj.model.compile(loss='categorical_crossentropy',
                                        optimizer=model_obj.optimizer,
                                        metrics=['accuracy'])

                # train the created model
                model_obj.train_model()


if __name__ == "__main__":
    main()
