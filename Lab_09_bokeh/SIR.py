import numpy as np
from scipy.integrate import odeint


def dydt(y: np.ndarray, t: np.ndarray, beta: float, gamma: float) -> list[float]:
    S, I, R = y

    return [-beta * S * I, beta * S * I - gamma * I, gamma * I]


def SIR(beta: float = 0.2, gamma: float = 0.05, t_max: int = 200) -> tuple:
    t = np.arange(0, t_max, 0.01)

    sol = odeint(
        func=dydt,
        y0=[0.990, 0.001, 0.00],
        t=t,
        args=(beta, gamma)
    )

    return t, sol[:, 0], sol[:, 1], sol[:, 2]


