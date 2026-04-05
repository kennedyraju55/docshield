"""Base agent class for all DocShield agents."""


class BaseAgent:
    def __init__(self, backend, name):
        self.backend = backend
        self.name = name

    def run(self, context):
        """Run the agent. Yields {"agent": name, "token": str} dicts.
        Final yield should include {"done": True, "result": full_text}.
        """
        raise NotImplementedError
