import os

from gym import envs, logger

SKIP_MUJOCO_WARNING_MESSAGE = (
    "Cannot run mujoco test (either license key not found or mujoco not"
    "installed properly)."
)


skip_mujoco = not (os.environ.get("MUJOCO_KEY"))
if not skip_mujoco:
    try:
        import mujoco_py
    except ImportError:
        skip_mujoco = True


def should_skip_env_spec_for_tests(spec):
    # We skip tests for envs that require dependencies or are otherwise
    # troublesome to run frequently
    ep = spec.entry_point
    # Skip mujoco tests for pull request CI
    if skip_mujoco and ep.startswith("gym.envs.mujoco"):
        return True
    try:
        import gym.envs.atari
    except ImportError:
        if ep.startswith("gym.envs.atari"):
            return True
    try:
        import Box2D
    except ImportError:
        if ep.startswith("gym.envs.box2d"):
            return True

    if (
        "GoEnv" in ep
        or "HexEnv" in ep
        or (
            ep.startswith("gym.envs.atari")
            and not spec.id.startswith("Pong")
            and not spec.id.startswith("Seaquest")
        )
    ):
        logger.warn(f"Skipping tests for env {ep}")
        return True
    return False


spec_list = [
    spec
    for spec in sorted(envs.registry.values(), key=lambda x: x.id)
    if spec.entry_point is not None and not should_skip_env_spec_for_tests(spec)
]
