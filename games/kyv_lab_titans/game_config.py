"""Template game configuration file, detailing required user-specified inputs."""

from src.config.config import Config
from src.config.distributions import Distribution
from src.config.config import BetMode


class GameConfig(Config):
    """Template configuration class."""

    def __init__(self):
        super().__init__()
        self.game_id = "kyv_lab_titans"
        self.provider_number = 0
        self.working_name = "Labyrinth of the Titans"
        self.wincap = 10000.0
        self.win_type = "cluster"
        self.rtp = 0.962
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 6
        self.num_rows = [6] * self.num_reels
        # Board and Symbol Properties
        t5, t6, t8, t10, t12, t15, t20 = (5, 5), (6, 7), (8, 9), (10, 11), (12, 14), (15, 19), (20, 36)
        pay_group = {
            (t5, "TR"): 0.5,
            (t6, "TR"): 0.8,
            (t8, "TR"): 1.6,
            (t10, "TR"): 3.0,
            (t12, "TR"): 6.0,
            (t15, "TR"): 12.0,
            (t20, "TR"): 25.0,
            (t5, "HE"): 0.4,
            (t6, "HE"): 0.6,
            (t8, "HE"): 1.2,
            (t10, "HE"): 2.0,
            (t12, "HE"): 4.0,
            (t15, "HE"): 8.0,
            (t20, "HE"): 16.0,
            (t5, "SH"): 0.3,
            (t6, "SH"): 0.5,
            (t8, "SH"): 1.0,
            (t10, "SH"): 1.8,
            (t12, "SH"): 3.5,
            (t15, "SH"): 7.0,
            (t20, "SH"): 12.0,
            (t5, "RR"): 0.2,
            (t6, "RR"): 0.3,
            (t8, "RR"): 0.6,
            (t10, "RR"): 1.2,
            (t12, "RR"): 2.0,
            (t15, "RR"): 4.0,
            (t20, "RR"): 8.0,
            (t5, "RB"): 0.2,
            (t6, "RB"): 0.3,
            (t8, "RB"): 0.6,
            (t10, "RB"): 1.2,
            (t12, "RB"): 2.0,
            (t15, "RB"): 4.0,
            (t20, "RB"): 8.0,
            (t5, "RG"): 0.2,
            (t6, "RG"): 0.3,
            (t8, "RG"): 0.6,
            (t10, "RG"): 1.2,
            (t12, "RG"): 2.0,
            (t15, "RG"): 4.0,
            (t20, "RG"): 8.0,
        }
        self.paytable = self.convert_range_table(pay_group)

        self.include_padding = True
        self.special_symbols = {"wild": ["W"], "scatter": ["S"], "collector": ["K"]}

        self.freespin_triggers = {
            self.basegame_type: {3: 10, 4: 12, 5: 15, 6: 20},
            self.freegame_type: {3: 5, 4: 5, 5: 5, 6: 5},
        }
        self.anticipation_triggers = {
            self.basegame_type: 2,
            self.freegame_type: 2,
        }
        # Reels
        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv"}
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(str.join("/", [self.reels_path, f]))

        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="basegame",
                        quota=1.0,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    )
                ],
            )
        ]
