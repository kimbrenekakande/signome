
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, RichLog, Input
from textual.containers import ScrollableContainer, VerticalScroll


class Biome(App):
    CSS_PATH = "src/css/style.tcss"
    """App comp"""
    def compose(self) -> ComposeResult:
        with VerticalScroll(id="input_area"):
            yield Input()
            yield Button("Start", id="submitter")

if __name__ ==  "__main__" :
    Biome().run()