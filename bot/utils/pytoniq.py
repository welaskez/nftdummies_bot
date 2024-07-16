from pytoniq import LiteBalancer, WalletV4R2

import config


async def get_wallet(provider: LiteBalancer):
    wallet, public_key, private_key, mnemonic = WalletV4R2.from_mnemonic(
        provider=provider,
        mnemonics=config.MNEMONICS,
    )

    return wallet, public_key, private_key, mnemonic
