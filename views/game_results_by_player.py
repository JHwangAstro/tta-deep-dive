import functools

import pandas as pd


def view(input_dataframes, **kwargs) -> pd.DataFrame:
    """ Dataframe mapping game results and starting place to game and player.
    """
    # Load the data from the url and rename columns.
    renamed_cols = {
        "division": "division",
        "position1": "1st position",
        "position2": "2nd position",
        "position3": "3rd position",
        "place1": "1st place",
        "points1": "1st points",
        "place2": "2nd place",
        "points2": "2nd points",
        "place3": "3rd place",
        "points3": "3rd points"
    }

    df = (
        functools.reduce(
            lambda df, item: df.assign(**{item[0]: df[item[1]]}),
            renamed_cols.items(),
            input_dataframes.get("game_results_with_seating")
        )
        [renamed_cols.keys()]
    )

    # Remove rows without data.
    filtered_df = (
        df
        .assign(game_id=tuple(range(len(df))))
        .assign(
            finish_points1=lambda df: tuple(
                (finish, points)
                for finish, points in zip(df.place1, df.points1)
            )
        )
        .assign(
            finish_points2=lambda df: tuple(
                (finish, points)
                for finish, points in zip(df.place2, df.points2)
            )
        )
        .assign(
            finish_points3=lambda df: tuple(
                (finish, points)
                for finish, points in zip(df.place3, df.points3)
            )
        )
        [df.division.notnull() & df.points3.notnull()]
    )

    # Create a long dataframe mapping
    # (division, game_id, player): start_position.
    start_position_df = (
        pd.melt(
            filtered_df,
            id_vars=["division", "game_id"],
            value_vars=["position1", "position2", "position3"],
            var_name="position_str",
            value_name="player"
        )
        .assign(
            position=lambda df: tuple(
                int(pos[-1])
                for pos in df.position_str
            )
        )
        .drop("position_str", axis=1)
        .reset_index(drop=True)
    )

    # Create a long dataframe mapping (game_id, player): (finish, points).
    # Encode the player with an integer.

    finish_df = (
        pd.melt(
            filtered_df,
            id_vars=["division", "game_id"],
            value_vars=["finish_points1", "finish_points2", "finish_points3"],
            var_name="finish_points_str",
            value_name="player_points"
        )
        .assign(player=lambda df: df.player_points.apply(lambda x: x[0]))
        .assign(points=lambda df: df.player_points.apply(lambda x: int(x[1])))
        .assign(
            finish=lambda df: tuple(
                int(pos[-1])
                for pos in df.finish_points_str
            )
        )
        .drop(["finish_points_str", "player_points"], axis=1)
        .reset_index(drop=True)
    )

    # Sort the divisions by player count - the higher skill divisions
    # have less players.
    # Due to the way the tournament is organized, the lowest division
    # actually has less players than the second lowest (not enough players
    # to fill the division), so we manually set this division to be
    # the lowest.

    ordered_divisions = (
        finish_df
        [["division", "player"]]
        .drop_duplicates()
        .groupby("division")
        .agg({"player": "count"})
        .reset_index()
        .assign(
            player_count=lambda df: tuple(
                count if division != "wood" else 10000000
                for count, division in zip(df.player, df.division)
            )
        )
        .sort_values("player_count", ascending=False)
        .reset_index()
        .division
        .to_list()
    )

    # Join the long dataframes to create a dataframe mapping:
    # (game_id, player): (start_position, finish, points)
    #
    # Order the divisions, as we may perform some cuts by skill level.

    finish_by_start_df = (
        finish_df.merge(
            start_position_df,
            on=["division", "game_id", "player"],
            how="inner"
        )
        .assign(player=lambda df: df.player.astype("category").cat.codes)
        .assign(
            division=pd.Categorical(
                finish_df.division,
                categories=ordered_divisions
            )
        )
    )

    return finish_by_start_df
