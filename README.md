# STM32F411 sem o framework do TCC

Implementação convencional com **STM32CubeF4 HAL v1.28.3**, CMSIS e GCC ARM. A HAL da ST continua sendo utilizada; não há dependência da HAL portável, arena, BSP ou componentes do framework do TCC. Este projeto pode ser copiado e compilado separadamente.

## Organização

- `Core/Inc`: cabeçalhos da aplicação, periféricos e configuração da HAL ST.
- `Core/Src/main.c`: `main`, `SystemClock_Config` e tratamento de falha de inicialização.
- `Core/Src/gpio.c`, `i2c.c`, `usart.c`, `tim.c`: funções `MX_*_Init` e handles nativos.
- `Core/Src/stm32f4xx_hal_msp.c`: clocks, funções alternativas e NVIC.
- `Core/Src/stm32f4xx_it.c`: exceções, SysTick e interrupção do TIM2.
- `Core/Src/system_stm32f4xx.c`, `syscalls.c`, `sysmem.c`, `Core/Startup` e `STM32F411CEUX_FLASH.ld`: suporte de execução Cortex-M4.
- `Drivers/CMSIS` e `Drivers/STM32F4xx_HAL_Driver`: código oficial instalado pelo script, preservando licenças.
- `Core/Src/application.c`: processamento sequencial de botão, aquisição, tela, LED e telemetria.
- `sht31d.c` e `ssd1306.c`: acesso direto a `HAL_I2C_Master_Transmit/Receive`; `telemetry.c` usa `HAL_UART_Transmit`.

A estrutura segue as convenções STM32Cube; os arquivos foram organizados manualmente, sem afirmar geração pelo CubeMX e sem um `.ioc` que não represente o projeto.

## Preparar e compilar

Instale CMake >= 3.22, Ninja e `arm-none-eabi-gcc` no `PATH`.

```sh
python3 tools/install_drivers.py
cmake --preset Debug
cmake --build --preset Debug
cmake --preset Release
cmake --build --preset Release
```

O instalador baixa revisões fixadas do STM32CubeF4 e preenche `Drivers/`. Para reutilizar um checkout limpo já instalado:

```sh
python3 tools/install_drivers.py --sdk /caminho/STM32CubeF4
```

Como alternativa ao preenchimento local, defina `STM32F4_SDK_DIR` com a raiz de uma instalação externa antes do CMake. Não é preciso ter os projetos com framework presentes. Os arquivos oficiais de `Drivers` instalados localmente são ignorados pelo Git; os scripts reproduzem a instalação.

Saídas em `build/Debug` e `build/Release`: `stm32f411_sem_framework.elf`, `.hex`, `.bin` e `.map`. Debug usa `-Og -g3`; Release usa `-O3`, sem LTO, mantendo assertions habilitadas, como a referência.

## Gravar

Com ST-LINK e STM32CubeProgrammer CLI instalados, a partir da raiz deste projeto:

```sh
STM32_Programmer_CLI -c port=SWD -w build/Debug/stm32f411_sem_framework.elf -v -rst
```

Para monitorar, utilize um adaptador USB-UART de **3,3 V**, conectado ao USART2, a 115200 8N1. Nenhuma gravação é realizada pelos comandos de compilação.

## Hardware e execução

| Função | Recurso |
| --- | --- |
| CPU | HSI + PLL, 100 MHz |
| Botão externo | PB0, ativo baixo, pull-up externo de 10 kΩ |
| LED externo | PB1, ativo alto, resistor série de 1 kΩ |
| I2C1 SCL / SDA | PB6 / PB7, 100 kHz, pull-ups externos |
| Sensor / display | SHT31-D `0x44` / SSD1306 `0x3C` |
| USART2 TX / RX | PA2 / PA3, 115200 8N1 |
| Base da aplicação | TIM2, interrupção nominal a cada 1 ms |

O SysTick alimenta os timeouts da HAL ST. `app_ticks` conta exclusivamente interrupções atendidas do TIM2, iniciado após a inicialização dos dispositivos e da aplicação. O laço principal não inclui esperas de conversão nem de intervalo; as transferências dos drivers são síncronas e têm timeout de 100 ms no I2C e 1000 ms na UART.

Comportamento, formato dos registros, recuperação, origem dos elementos gráficos e limitações de validação estão em [SEM_FRAMEWORK.md](https://github.com/fmsantos8/testes_framework/blob/main/docs/SEM_FRAMEWORK.md). O LED fica apagado durante a inicialização; falha de inicialização entra em `Error_Handler`. Os ensaios de desconexão pressupõem inicialização bem-sucedida.


## Evidências da avaliação

Os fontes e as configurações desta publicação correspondem aos arquivos identificados nos builds de 02/11/2026 e na campanha de 07–08/11/2026. A configuração comparada no artigo é Debug (-Og). Os binários avaliados, métricas, registros e o manifesto que relaciona seus hashes aos commits publicados estão em [testes_framework](https://github.com/fmsantos8/testes_framework). Este repositório contém a implementação convencional; sua compilação não depende do framework proposto.
