import json
import os


def test_provider_number_used_in_backend_config(tmp_path, monkeypatch):
    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    monkeypatch.syspath_prepend(str(project_root))
    monkeypatch.syspath_prepend(str(project_root / "games" / "kyv_lab_titans"))

    from games.kyv_lab_titans.game_config import GameConfig
    from games.kyv_lab_titans.gamestate import GameState
    from src.config import paths as paths_module
    from src.config import output_filenames
    from src.write_data.write_configs import generate_configs
    from src.write_data import write_configs

    # Initialize config and ensure provider number is set as expected
    config = GameConfig()
    assert config.provider_number == 0

    # Redirect output paths to temporary directory
    monkeypatch.setattr(paths_module, "PATH_TO_GAMES", tmp_path)
    monkeypatch.setattr(output_filenames, "PATH_TO_GAMES", tmp_path)
    config.construct_paths()

    # Patch heavy distribution calculations
    monkeypatch.setattr(write_configs, "make_win_distribution", lambda *args, **kwargs: {0.0: 1.0})
    monkeypatch.setattr(write_configs, "get_lookup_length", lambda *args, **kwargs: 1)
    monkeypatch.setattr(write_configs, "get_distribution_moments", lambda *args, **kwargs: (0.0, 0.0, 0.0, 0.0))

    gamestate = GameState(config)

    # Create minimal files required for backend config generation
    base_lookup_path = gamestate.output_files.lookups["base"]["paths"]["base_lookup"]
    optimized_lookup_path = gamestate.output_files.lookups["base"]["paths"]["optimized_lookup"]
    force_record_path = gamestate.output_files.force["base"]["paths"]["force_record"]
    force_json_path = os.path.join(gamestate.output_files.force_path, "force.json")

    for path in [base_lookup_path, optimized_lookup_path, force_record_path, force_json_path]:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    for path in [base_lookup_path, optimized_lookup_path]:
        with open(path, "w", encoding="utf-8") as f:
            f.write("0,1,0\n")

    with open(force_record_path, "w", encoding="utf-8") as f:
        f.write("{}")

    with open(force_json_path, "w", encoding="utf-8") as f:
        f.write("{}")

    generate_configs(gamestate)

    backend_config_path = gamestate.output_files.configs["paths"]["be_config"]
    with open(backend_config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["providerNumber"] == 0
