import time


class CircuitBreaker:
    """
    Implementación simple de un Circuit Breaker.
    """
    def __init__(self, failure_threshold=3, recovery_time=30):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time

        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"

    def can_execute(self) -> bool:
        """
        Verifica si se puede ejecutar la operación protegida.

        outputs:
            bool: True si se puede ejecutar, False si el circuito está abierto.
        """
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_time:
                self.state = "HALF_OPEN"
                return True
            return False
        return True

    def record_success(self):
        """
        Registra una ejecución exitosa y resetea el contador de fallos.
        """
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self):
        """
        Registra una ejecución fallida y actualiza el estado del circuito.
        """
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
