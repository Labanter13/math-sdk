"""Game specific calculation helpers for Labyrinth of the Titans."""

from src.executables.executables import Executables
from src.calculations.cluster import Cluster


class GameCalculations(Executables):
    """Collection of helper methods used by the game executables."""

    # --- Cascade / win evaluation -------------------------------------------------
    def evaluate_cascade(self) -> None:
        """Evaluate current board, update wins and collect keys."""
        clusters = Cluster.get_clusters(self.board, "wild")
        return_data = {"totalWin": 0, "wins": []}
        self.board, self.win_data, _ = Cluster.evaluate_clusters(
            self.config,
            self.board,
            clusters,
            global_multiplier=self.global_multiplier,
            return_data=return_data,
        )

        Cluster.record_cluster_wins(self)
        self.win_manager.update_spinwin(self.win_data["totalWin"])
        self.win_manager.tumble_win = self.win_data["totalWin"]

        # Collect any keys on the evaluated board for future wild spawns / boosts.
        self.collect_keys()

    # --- Multiplier ladder --------------------------------------------------------
    def update_multiplier_ladder(self) -> None:
        """Increase global multiplier based on collected keys."""
        if not hasattr(self, "keys_collected"):
            self.keys_collected = 0

        # Define a simple ladder where every 3 keys grants +1 multiplier.
        ladder_step = int(self.keys_collected / 3)
        target_mult = 1 + ladder_step

        while self.global_multiplier < target_mult:
            self.update_global_mult()

    # --- Key collection -----------------------------------------------------------
    def collect_keys(self) -> None:
        """Store positions of key symbols for later wild spawning."""
        if not hasattr(self, "keys_collected"):
            self.keys_collected = 0
        if not hasattr(self, "pending_wilds"):
            self.pending_wilds = []

        for reel, _ in enumerate(self.board):
            for row, symbol in enumerate(self.board[reel]):
                if symbol.name == "K" or symbol.check_attribute("collector"):
                    self.keys_collected += 1
                    self.pending_wilds.append({"reel": reel, "row": row})

