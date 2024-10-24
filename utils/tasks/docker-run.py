#!/usr/bin/env python3

import argparse
import subprocess
import os
import sys


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Run the local docker image, see the Taskfile.yml for usage."
    )
    parser.add_argument(
        "--volume",
        action="append",
        help=(
            "Specify additional volume(s) to mount in the Docker container. "
            "Can be specified multiple times."
        ),
        metavar="VOLUME",
    )
    parser.add_argument(
        "other_arguments",
        nargs=argparse.REMAINDER,
        help="Additional arguments to pass to the Docker command.",
    )
    return parser.parse_args()


def main():
    arguments = get_arguments()

    # Print the action being taken
    print("Running docker run")

    # Note: Ensure any setup from 'utils/tasks/docker-setup.sh' is handled elsewhere.

    # Base Docker command
    docker_command = [
        "docker",
        "run",
        "--interactive",
        "--tty",
        "--rm",
        "--volume",
        f"{os.getcwd()}:/builds/worker/checkouts",
        "--workdir",
        "/builds/worker/checkouts",
    ]

    # Add additional volumes if provided
    if arguments.volume:
        for volume in arguments.volume:
            docker_command.extend(["--volume", volume])

    # Specify the Docker image
    docker_command.append("ftt-local")

    # Append any additional arguments
    if arguments.other_arguments:
        docker_command.extend(arguments.other_arguments)

    print("Executing command:", " ".join(docker_command))
    result = subprocess.run(docker_command, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
