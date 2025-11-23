import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


"""
Copyright

The dataset of this repo comes from: https://github.com/KeithGalli/pandas/blob/master/pokemon_data.csv
"""

def draw_figure(cm, target_names):
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        xticklabels=target_names,
        yticklabels=target_names
    )
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.title("Confusion Matrix (SVM on Top-5 Type 1)")
    plt.tight_layout()
    plt.show()


def main():
    # Step 1. Data process and analysis
    df = pd.read_csv("/Users/hannyares/ML_tutorial/pokemon_data.csv")
    type_counts = df["Type 1"].value_counts()
    top5_type = type_counts.head(5).index.tolist()
    df_top5 = df[df["Type 1"].isin(top5_type)].copy()
    feature_cols = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed",
                "Generation", "Legendary"]
    df_top5["Legendary"] = df_top5["Legendary"].astype(int)
    X = df_top5[feature_cols].values   # Features
    y_raw = df_top5["Type 1"].values   # Lable  & Target

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)

    # Step 2. Split the train and test set (validation is occasionally need)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,       # 4:1 => test_size = 1 / (4+1) = 0.2
        random_state=42,
        stratify=y          
    )

    # Step 3. Normalize
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)   # 只在训练集上 fit
    X_test_scaled = scaler.transform(X_test)        # 测试集只做 transform

    # Step 4.Fit the ML model
    model = SVC(
        kernel="rbf",
        C=1.0,
        gamma="scale",
        random_state=42
    )
    model.fit(X_train_scaled, y_train)

    # Step 5. Predict
    y_pred = model.predict(X_test_scaled)

    # Step 6. Evaluate
    acc = accuracy_score(y_test, y_pred)
    print("Accuracy on test set: {:.4f}".format(acc))

    print("\nClassification Report:")
    target_names = label_encoder.classes_
    print(classification_report(y_test, y_pred, target_names=target_names))

    cm = confusion_matrix(y_test, y_pred)

    draw_figure(cm, target_names)


if __name__ == "__main__":
    main()



