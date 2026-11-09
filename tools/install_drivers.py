#!/usr/bin/env python3
"""Populate the conventional Drivers layout from the pinned STM32CubeF4."""
import argparse
from pathlib import Path
import shutil
import tempfile
import subprocess
import sys
from install_stm32f4_sdk import verify
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--sdk', type=Path, help='Existing clean STM32CubeF4 v1.28.3 checkout')
a = p.parse_args()
project = Path(__file__).resolve().parents[1]
def install(sdk):
    verify(sdk)
    drivers = project / 'Drivers'
    if any((drivers / name).exists() for name in ['CMSIS/Include/core_cm4.h', 'STM32F4xx_HAL_Driver/Inc/stm32f4xx_hal.h']):
        raise SystemExit('Drivers already populated. Use STM32F4_SDK_DIR for another SDK; existing files are preserved.')
    for relative in ['CMSIS/Include', 'CMSIS/Device/ST/STM32F4xx', 'STM32F4xx_HAL_Driver']:
        shutil.copytree(sdk / 'Drivers' / relative, drivers / relative, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('.git'))
    for name in ['LICENSE.md', 'LICENSE.txt', 'LICENSE']:
        if (sdk / name).exists(): shutil.copyfile(sdk / name, drivers / ('STM32CubeF4-' + name))
    print('Installed STM32CubeF4 v1.28.3 in', drivers)
if a.sdk:
    install(a.sdk.resolve())
else:
    with tempfile.TemporaryDirectory(prefix='tcc-cube-') as temporary:
        sdk = Path(temporary) / 'STM32CubeF4'
        subprocess.run([sys.executable, str(project / 'tools/install_stm32f4_sdk.py'), str(sdk)], check=True)
        install(sdk)
