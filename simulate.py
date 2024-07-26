INIT_REAL_TOKEN_RESERVE = 793_100_000 * 10**18
CORE_PRICE = 1.52 # 1 CORE is 1.52 dollars

def calculate_y(start_price_core: float, init_real_token_reserve: float, target_mcap_core: float):
    return (((start_price_core*init_real_token_reserve - start_price_core + target_mcap_core*init_real_token_reserve)/target_mcap_core) + (1 * 10**18)) * start_price_core

def calculate_k1(start_price_core: float, init_real_token_reserve: float, target_mcap_core: float):
    return ((start_price_core*init_real_token_reserve - start_price_core + target_mcap_core*init_real_token_reserve)/target_mcap_core)

def calculate_z(k1: float, start_price: float):
    return start_price*(k1*k1 + k1)

def calculate_token_variables(start_price_usd: float, target_mcap_usd: float):
    target_mcap_in_core = target_mcap_usd
    start_price_core = start_price_usd
    # init_virtual_token_reserve = (start_price_core * INIT_REAL_TOKEN_RESERVE/target_mcap_in_core)
    # init_virtual_eth_reserve = start_price_core * init_virtual_token_reserve
    # curve_constant = init_virtual_token_reserve * init_virtual_eth_reserve
    init_virtual_eth_reserve = calculate_y(start_price_core, INIT_REAL_TOKEN_RESERVE, target_mcap_in_core)
    init_virtual_token_reserve = calculate_k1(start_price_core, INIT_REAL_TOKEN_RESERVE, target_mcap_in_core)
    curve_constant = calculate_z(init_virtual_token_reserve, start_price_core)
    return {
        "curve_constant": curve_constant,
        "init_virtual_token_reserve": init_virtual_token_reserve,
        "init_virtual_eth_reserve": init_virtual_eth_reserve,
    }

def calculate_amount_out_from_usd(amount_in_usd: float, v_eth_reserve: float, v_token_reserve: float, curve_constant: float):
    amount_in_core = amount_in_usd
    new_v_eth_reserve = v_eth_reserve + amount_in_core
    new_v_token_reserve = curve_constant/new_v_eth_reserve
    return v_token_reserve - new_v_token_reserve

token_variables = calculate_token_variables(1*10**18, 100*10**18)
print(token_variables)
amount_out = calculate_amount_out_from_usd(1*10**18, token_variables['init_virtual_eth_reserve'], token_variables['init_virtual_token_reserve'], token_variables['curve_constant'])
print(amount_out)