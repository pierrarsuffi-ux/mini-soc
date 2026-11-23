"""Entraîne et évalue un modèle supervisé (Random Forest) de détection d'attaques."""

import duckdb
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split

from ingest import DB_FILE

FEATURE_COLUMNS = ["hour", "is_failed", "ip_nb_attempts", "ip_nb_usernames", "ip_fail_rate"]


def load_features():
    """Lit la table features : renvoie les features (X) et la vérité (y)."""
    query = f"SELECT {', '.join(FEATURE_COLUMNS)}, label FROM features"
    with duckdb.connect(DB_FILE, read_only=True) as con:
        rows = con.execute(query).fetchall()

    X = []
    y = []
    for row in rows:
        X.append(row[:-1])
        y.append(0 if row[-1] == "normal" else 1)
    return X, y


def main():
    X, y = load_features()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print(f"Entraînement : {len(X_train)} connexions, test : {len(X_test)} connexions")
    print(f"Précision : {precision_score(y_test, y_pred):.2f}")
    print(f"Rappel    : {recall_score(y_test, y_pred):.2f}")
    print("Matrice de confusion :")
    print(confusion_matrix(y_test, y_pred))

    print("Importance des features :")
    for name, importance in zip(FEATURE_COLUMNS, model.feature_importances_):
        print(f"  {name:<16} {importance:.2f}")


if __name__ == "__main__":
    main()