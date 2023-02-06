from starlette.requests import Request

from app.core import BitcoinWalletCore


def get_core(request: Request) -> BitcoinWalletCore:
    core: BitcoinWalletCore = request.app.state.core
    return core
