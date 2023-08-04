import datetime
import pickle

import pandas as pd
from river import metrics, stream


def create_user_uid():
    now = datetime.datetime.now()
    user_id = now.strftime("%Y%m%d%H%M%S")
    user_id = int(user_id)

    return user_id


def create_dataset(rated_anime):
    rated_anime_df = pd.DataFrame(rated_anime)
    rated_anime_df.rename(columns={0: "Name_lower"}, inplace=True)

    # Get anime id
    anime_list = pd.read_csv("../data/anime_list.csv")
    anime_list["Name_lower"] = anime_list["Name"].str.lower()
    rated_anime_df = pd.merge(
        rated_anime_df,
        anime_list[["anime_id", "Name_lower"]],
        on="Name_lower",
        how="left",
    )
    rated_anime_ids = rated_anime_df["anime_id"]

    # Create user id
    user_id = create_user_uid()

    # Rating
    # スコアは入力してもらはない想定なので最高得点を付与
    rated_anime_df["user_id"] = user_id
    rated_anime_df["rating"] = 10

    # Create river dataset
    X = rated_anime_df[["user_id", "anime_id"]]
    y = rated_anime_df[["rating"]]
    dataset = stream.iter_pandas(X, y)

    return anime_list, user_id, rated_anime_ids, dataset


def online_learning(dataset):
    # Load pretrained model
    with open("../data/model.pkl", "rb") as f:
        model = pickle.load(f)

    # Update model
    metric = metrics.MAE() + metrics.RMSE()
    for x, y in dataset:
        y_pred = model.predict_one(user=x["user_id"], item=x["anime_id"])
        metric = metric.update(y["rating"], y_pred)
        model = model.learn_one(user=x["user_id"], item=x["anime_id"], y=y["rating"])
    print(metric)

    return model


def predict(model, user_id, anime_list, rated_anime_ids):
    # predict recommend item
    result_df = model.rank(user=user_id, items=anime_list["anime_id"])
    result_df = pd.DataFrame(result_df, columns=["anime_id"])
    result_df = pd.merge(result_df, anime_list, on=["anime_id"], how="inner")

    # # remove rated item
    result_df = result_df[~result_df["anime_id"].isin(rated_anime_ids)]
    result_df = result_df.reset_index(drop=True)[0:10]

    return result_df


def get_recommend_result(rated_anime):
    anime_list, user_id, rated_anime_ids, dataset = create_dataset(rated_anime)
    model = online_learning(dataset)
    recommend_result = predict(model, user_id, anime_list, rated_anime_ids)

    return recommend_result
