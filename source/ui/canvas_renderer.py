import tkinter as tk
import abc

class CanvasRenderer(abc.ABC):
    @abc.abstractmethod
    def update_canvas(self, canvas: tk.Canvas):
        ...
