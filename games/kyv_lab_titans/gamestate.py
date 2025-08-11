"""Handles the state and output for a single simulation round"""

from game_override import GameStateOverride


class GameState(GameStateOverride):
    """Handle all game-logic and event updates for a given simulation number."""

    def run_spin(self, sim):
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            # Reset simulation and key tracking for a new spin
            self.reset_book()
            self.keys_collected = 0
            self.pending_wilds = []

            self.draw_board()
            self.spawn_wilds()
            self.evaluate_cascade()
            self.emit_tumble_win_events()
            self.handle_key_boosts()

            while self.win_data["totalWin"] > 0 and not (self.wincap_triggered):
                self.tumble_game_board()
                self.spawn_wilds()
                self.evaluate_cascade()
                self.emit_tumble_win_events()
                self.handle_key_boosts()

            self.set_end_tumble_event()
            self.win_manager.update_gametype_wins(self.gametype)

            if self.check_fs_condition() and self.check_freespin_entry():
                self.run_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self):
        self.reset_fs_spin()
        while self.fs < self.tot_fs:
            self.update_freespin()
            self.spawn_wilds()
            self.evaluate_cascade()
            self.emit_tumble_win_events()
            self.handle_key_boosts()

            while self.win_data["totalWin"] > 0 and not (self.wincap_triggered):
                self.tumble_game_board()
                self.spawn_wilds()
                self.evaluate_cascade()
                self.emit_tumble_win_events()
                self.handle_key_boosts()

            self.set_end_tumble_event()
            self.win_manager.update_gametype_wins(self.gametype)

            if self.check_fs_condition():
                self.update_fs_retrigger_amt()

        self.end_freespin()
