# Esempio: risoluzione numerica di un problema di ottimizzazione
# vincolata con il metodo del gradiente proiettato.

import numpy as np


def projected_gradient(grad, project, x0, step=0.01, tol=1e-6, max_iter=1000):
    """Minimizza una funzione tramite gradiente proiettato.

    grad: funzione che restituisce il gradiente nel punto x
    project: funzione di proiezione sul dominio ammissibile
    x0: punto iniziale
    """
    x = x0
    for _ in range(max_iter):
        x_new = project(x - step * grad(x))
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    return x


if __name__ == "__main__":
    grad = lambda x: 2 * x - np.array([4.0, 4.0])
    project = lambda x: np.clip(x, 0, None)  # vincolo x >= 0

    x_star = projected_gradient(grad, project, x0=np.zeros(2))
    print(f"Soluzione trovata: {x_star}")
