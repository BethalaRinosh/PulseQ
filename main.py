"""Launch the PulseQ academic command-line demonstration."""

from pulseq.cli import PulseQApp


def main() -> None:
    PulseQApp().run()


if __name__ == "__main__":
    main()
