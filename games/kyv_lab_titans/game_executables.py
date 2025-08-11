"""Executable helpers for Labyrinth of the Titans."""

from game_calculations import GameCalculations


class GameExecutables(GameCalculations):
    """Grouped game actions triggered during play."""

    # --- Wild spawning ------------------------------------------------------------
    def spawn_wilds(self) -> None:
        """Replace collected key positions with wild symbols."""
        if not hasattr(self, "pending_wilds"):
            self.pending_wilds = []
        for pos in self.pending_wilds:
            self.board[pos["reel"]][pos["row"]] = self.create_symbol("W")
        self.pending_wilds = []

    # --- Key boosts ---------------------------------------------------------------
    def handle_key_boosts(self) -> None:
        """Apply multiplier ladder after key collection."""
        self.update_multiplier_ladder()

    # --- Free spin behaviour ------------------------------------------------------
    def update_freespin(self) -> None:
        """Persist multiplier while preparing new free spin."""
        super().update_freespin()

