from pytonapi.exceptions import (
    TONAPIError,
    TONAPIInternalServerError,
    TONAPIServerError,
)
from pytonapi import AsyncTonapi

import config

tonapi = AsyncTonapi(api_key=config.TONAPI_API_KEY)


async def get_rates(jettton_master_address: str, retry_count: int = 3):
    try:
        rates = await tonapi.rates.get_prices(
            tokens=[jettton_master_address], currencies=["usd", "ton"]
        )
    except (TONAPIError, TONAPIInternalServerError, TONAPIServerError):
        if retry_count > 0:
            return await get_rates(jettton_master_address, retry_count - 1)
        return
    except Exception as e:
        print(f"Error with getting rates: {e}")
        return

    price_usd = rates.rates[jettton_master_address]["prices"]["USD"]
    price_ton = rates.rates[jettton_master_address]["prices"]["TON"]
    diff_24h = rates.rates[jettton_master_address]["diff_24h"]["USD"]
    diff_7d = rates.rates[jettton_master_address]["diff_7d"]["USD"]
    diff_30d = rates.rates[jettton_master_address]["diff_30d"]["USD"]

    formatted_price_usd = f"{price_usd:.10f}"
    formatted_price_ton = f"{price_ton:.10f}"
    if formatted_price_usd.count("0") < 7:
        formatted_price_usd = round(price_usd, 6)
        formatted_price_ton = round(price_ton, 7)

    return (
        formatted_price_usd,
        formatted_price_ton,
        diff_24h,
        diff_7d,
        diff_30d,
    )
