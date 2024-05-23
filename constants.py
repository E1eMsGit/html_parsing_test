 # -*- coding: utf-8 -*-
"""
Модуль констант.
=======================================================
* Содержит константы для программы парсинга html файлов;
=======================================================
"""
from typing import Final


class Constants:
    """
    Перечень констант.
    """
    ZERO: Final = '0'
    CE: Final = 'C'
    V_TMSH: Final = "[B.TMШ   ]"
    ED_TMSH: Final = "[EД.TMШ  ]"
    PRD_O: Final = "ПРД-О"
    PRD_R: Final = "ПРД-Р"
    KV_F: Final = "Гц"
    INTER: Final = "интрлвг"
    FCP_O: Final = "осн.ФЦП"
    FCP_R: Final = "рез.ФЦП"

    # Каналы.
    CH1_ON_CMD: Final = 'ПСК1'
    CH1_OFF_CMD: Final = 'ОСК1'
    CH2_ON_CMD: Final = 'ПСК2'
    CH2_OFF_CMD: Final = 'ОСК2'
    CH3_ON_CMD: Final = 'ПСК3'
    CH3_OFF_CMD: Final = 'ОСК3'
    CH4_ON_CMD: Final = 'ПСК4'
    CH4_OFF_CMD: Final = 'ОСК4'
    CH5_ON_CMD: Final = 'ПСК5'
    CH5_OFF_CMD: Final = 'ОСК5'
    CH6_ON_CMD: Final = 'ПСК6'
    CH6_OFF_CMD: Final = 'ОСК6'
    CHANNELS_STATUSES: Final = [[CH1_ON_CMD, CH1_OFF_CMD],[CH2_ON_CMD, CH2_OFF_CMD],[CH3_ON_CMD, CH3_OFF_CMD],
                               [CH4_ON_CMD, CH4_OFF_CMD],[CH5_ON_CMD, CH5_OFF_CMD],[CH6_ON_CMD, CH6_OFF_CMD]]


if __name__ == "__main__":
    print("Use main.py file!")
    
