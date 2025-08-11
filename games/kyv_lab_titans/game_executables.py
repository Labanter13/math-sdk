from game_calculations import GameCalculations
from src.calculations.cluster import Cluster


class GameExecutables(GameCalculations):
    """Game specific grouped helper functions."""

    def get_clusters_update_wins(self) -> None:
        """Evaluate all clusters on the current board and update win manager."""
        clusters = Cluster.get_clusters(self.board, "wild")
        return_data = {"totalWin": 0, "wins": []}
        self.board, self.win_data, total_win = Cluster.evaluate_clusters(
            config=self.config,
            board=self.board,
            clusters=clusters,
            global_multiplier=self.global_multiplier,
            return_data=return_data,
        )
        self.win_manager.update_spinwin(total_win)
        self.win_manager.tumble_win = total_win

