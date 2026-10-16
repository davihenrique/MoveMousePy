"""Move o mouse periodicamente para manter o computador ativo.

Uso:
    python move_mouse.py            # move a cada 5 segundos (padrao)
    python move_mouse.py 30         # move a cada 30 segundos
    python move_mouse.py 30 -r 100  # a cada 30 segundos, circulo com raio de 100 pixels

Pressione Ctrl+C para encerrar.
"""

import argparse
import ctypes
import math
import time
from ctypes import wintypes
from datetime import datetime

MOUSEEVENTF_MOVE = 0x0001
DEFAULT_INTERVAL = 5.0
DEFAULT_RADIUS = 50


def move_mouse_in_circle(radius: int = DEFAULT_RADIUS, steps: int = 36, duration: float = 0.5) -> None:
    """Move o mouse fazendo um circulo e volta para a posicao original.

    A posicao atual do cursor e um ponto do circulo. Usa posicoes absolutas
    (SetCursorPos) para nao sofrer com a aceleracao do mouse, e um mouse_event
    (input real) a cada passo para reiniciar o contador de inatividade do Windows.
    """
    user32 = ctypes.windll.user32
    start = wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(start))
    center_x = start.x - radius
    for i in range(1, steps + 1):
        angle = 2 * math.pi * i / steps
        user32.SetCursorPos(
            round(center_x + radius * math.cos(angle)),
            round(start.y + radius * math.sin(angle)),
        )
        user32.mouse_event(MOUSEEVENTF_MOVE, 0, 0, 0, 0)
        time.sleep(duration / steps)
    user32.SetCursorPos(start.x, start.y)


def positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("o intervalo deve ser maior que zero")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(description="Move o mouse periodicamente.")
    parser.add_argument(
        "intervalo",
        nargs="?",
        type=positive_float,
        default=DEFAULT_INTERVAL,
        help=f"intervalo em segundos entre os movimentos (padrao: {DEFAULT_INTERVAL:g})",
    )
    parser.add_argument(
        "-r",
        "--raio",
        type=int,
        default=DEFAULT_RADIUS,
        help=f"raio do circulo em pixels (padrao: {DEFAULT_RADIUS})",
    )
    args = parser.parse_args()
    if args.raio <= 0:
        parser.error("o raio deve ser maior que zero")

    print(
        f"Movendo o mouse em circulo (raio {args.raio}px) a cada {args.intervalo:g} segundo(s). "
        "Pressione Ctrl+C para sair."
    )
    try:
        while True:
            move_mouse_in_circle(args.raio)
            print(f"[{datetime.now():%H:%M:%S}] circulo feito")
            time.sleep(args.intervalo)
    except KeyboardInterrupt:
        print("\nEncerrado.")


if __name__ == "__main__":
    main()
