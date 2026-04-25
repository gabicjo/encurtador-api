from source.models import redirect_model


def add_new_click(code: str) -> None:
    redirect_model.add_new_click(code)