from abc import abstractmethod, ABC


class PenaltyCalculator(ABC):
    @abstractmethod
    def calculate(self, past_tickets_count: int) -> float:
        pass


class SimplePenaltyCalculator(PenaltyCalculator):
    def calculate(self, past_tickets_count: int) -> float:
        base = 100

        # Ejemplo de reglas de negocio
        if 0 < past_tickets_count < 4:
            base += 50
        if 4 < past_tickets_count < 11:
            base += 50
        else:
            base += 50

        return base
