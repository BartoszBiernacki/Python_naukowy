from numba import njit, prange
import numpy as np


@njit("i1[:, :](u2, f8)", parallel=True)
def make_grid(side_length: int, spin_up_density: float):
    grid = np.random.rand(int(side_length * side_length))
    grid = (grid < spin_up_density).astype(np.int8)
    grid[grid == 0] = -1
    grid = grid.reshape(side_length, -1)
    return grid


@njit("f8(i1[:, :], f8, f8)",
      cache=True, fastmath=True, parallel=True)
def calculate_hamiltonian_explicitly(
        grid: np.ndarray,
        J: float,
        B: float,
):
    nrows, ncols = grid.shape
    hamiltonian = 0.

    # Don't iterate over last row because row+1 is out of range.
    # Same about columns
    for row in prange(nrows - 1):
        for col in range(ncols - 1):
            me = grid[row, col]
            up = grid[row - 1, col]
            down = grid[row + 1, col]
            left = grid[row, col - 1]
            right = grid[row, col + 1]

            hamiltonian += -J * (
                    me * up + me * down + me * left + me * right) - B * me

    # Now iterate over last row and then last column but except for
    # value in down right corner of an array.
    row = nrows - 1
    for col in range(ncols - 1):
        me = grid[row, col]
        up = grid[row - 1, col]
        down = grid[0, col]
        left = grid[row, col - 1]
        right = grid[row, col + 1]

        hamiltonian += -J * (
                me * up + me * down + me * left + me * right) - B * me

    col = ncols - 1
    for row in range(nrows - 1):
        me = grid[row, col]
        up = grid[row - 1, col]
        down = grid[row + 1, col]
        left = grid[row, col - 1]
        right = grid[row, 0]

        hamiltonian += -J * (
                me * up + me * down + me * left + me * right) - B * me

    # Now value in down right corner of an array.
    row, col = nrows - 1, ncols - 1

    me = grid[row, col]
    up = grid[row - 1, col]
    down = grid[0, col]
    left = grid[row, col - 1]
    right = grid[row, 0]

    hamiltonian += -J * (
            me * up + me * down + me * left + me * right) - B * me

    return hamiltonian / 2


@njit("i1[:](i1[:, :], u2, u2)")
def neighbours_states(arr:  np.ndarray, row: int, col: int) -> np.ndarray:

    rows, cols = arr.shape

    l = arr[row, col-1]
    r = arr[row, (col+1) % cols]
    u = arr[row-1, col]
    d = arr[(row+1) % rows, col]

    return np.array([l, r, u, d])


@njit("f8(i1, i1[:], f8, f8)")
def hamiltonian_part(me, neighbors, B, J):
    return -J * sum(me*neighbors) - B*me


@njit("f8(i1[:, :], u2, u2, f8, f8)", cache=True, fastmath=True)
def hamiltonian_change_after_mikro_step(
        grid: np.ndarray,
        row: int,
        col: int,
        J: float,
        B: float,
):

    original_spin_value = grid[row, col]
    neighbours = neighbours_states(arr=grid, row=row, col=col)

    old_part = hamiltonian_part(
        me=original_spin_value,
        neighbors=neighbours, B=B, J=J)

    # Spin change
    new_part = hamiltonian_part(
        me=-original_spin_value,
        neighbors=neighbours, B=B, J=J)

    return -old_part + new_part


@njit("void(i1[:, :], f8, f8, f8)", cache=True, fastmath=True)
def mikro_step_MC(
        grid: np.ndarray,
        J: float,
        B: float,
        beta: float,
):
    nrows, ncols = grid.shape

    row = np.random.randint(0, nrows)
    col = np.random.randint(0, ncols)

    hamiltonian_change = hamiltonian_change_after_mikro_step(
        grid=grid, row=row, col=col, J=J, B=B,
    )

    if np.exp(-beta * hamiltonian_change) < np.random.rand():
        grid[row, col] = -grid[row, col]


@njit("void(i1[:, :], f8, f8, f8)", cache=True, fastmath=True, parallel=True)
def makro_step_MC(grid, J, B, beta):
    for _ in prange(grid.size):
        mikro_step_MC(grid=grid, J=J, B=B, beta=beta)




