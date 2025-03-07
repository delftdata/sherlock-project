import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import model_from_json
from pathlib import Path


def categorize_features() -> dict:
    """Get feature identifiers per feature set, to map features to feature sets.
    
    Returns
    -------
    feature_cols_dict
        Dictionary with lists of feature identifiers per feature set.
    """
    feature_cols_dict = {}
    for feature_set in ['char', 'word', 'par', 'rest']:
        feature_cols_dict[feature_set] = pd.read_csv(
            Path(__file__).parent.parent / 'features' / 'feature_column_identifiers' / f'{feature_set}_col.tsv',
            sep='\t', index_col=0, header=None, squeeze=True,
        ).to_list()
    return feature_cols_dict


def construct_sherlock_model(nn_id: str, with_weights: bool):
    """Load model architecture and populate with pretrained weights.
    
    Parameters
    ----------
    nn_id
        Identifier for retrained model.
    with_weights
        Whether to populate the model with trained weights.
    
    Returns
    -------
    sherlock_model
        Compiled sherlock model.
    callbacks
        Callback configuration for model retraining.
    """

    lr = 0.0001
    callbacks = [EarlyStopping(monitor="val_loss", patience=5)]

    with open(Path(__file__).parent.parent.parent / 'models' / 'sherlock_model.json', "r") as file:
        sherlock_model = model_from_json(file.read())
    
    if with_weights:
        model_path = Path(__file__).parent.parent.parent / 'models' / f"{nn_id}_weights.h5"
        sherlock_model.load_weights(str(model_path.resolve()))
        
    sherlock_model.compile(
        optimizer=tf.keras.optimizers.Adam(lr=lr),
        loss='categorical_crossentropy',
        metrics=['categorical_accuracy']
    )

    return sherlock_model, callbacks
