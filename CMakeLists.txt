cmake_minimum_required(VERSION 3.22)
set(CMAKE_TOOLCHAIN_FILE "${CMAKE_CURRENT_LIST_DIR}/cmake/gcc-arm-none-eabi.cmake" CACHE FILEPATH "Toolchain")
project(stm32f411_sem_framework LANGUAGES C ASM)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build configuration" FORCE)
endif()
add_executable(${PROJECT_NAME})
set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".elf")
set(cpu_flags -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard)
target_compile_options(${PROJECT_NAME} PRIVATE ${cpu_flags} -ffunction-sections -fdata-sections -Wall -Wextra -Wpedantic
    $<$<CONFIG:Debug>:-Og;-g3> $<$<CONFIG:Release>:-O3> -UNDEBUG)
target_compile_definitions(${PROJECT_NAME} PRIVATE STM32F411xE USE_HAL_DRIVER)
target_include_directories(${PROJECT_NAME} PRIVATE Core/Inc)
target_sources(${PROJECT_NAME} PRIVATE
    Core/Src/system_stm32f4xx.c Core/Src/main.c Core/Src/gpio.c Core/Src/i2c.c Core/Src/usart.c Core/Src/tim.c
    Core/Src/stm32f4xx_hal_msp.c Core/Src/stm32f4xx_it.c Core/Src/syscalls.c Core/Src/sysmem.c
    Core/Src/application.c Core/Src/sht31d.c Core/Src/ssd1306.c Core/Src/telemetry.c
    Core/Src/graphics.c Core/Src/fonts.c Core/Src/render.c Core/Src/bitmaps.c
    Core/Startup/startup_stm32f411xx.s)
add_subdirectory(Drivers)
target_link_options(${PROJECT_NAME} PRIVATE ${cpu_flags} --specs=nano.specs --specs=nosys.specs
    -T${CMAKE_CURRENT_SOURCE_DIR}/STM32F411CEUX_FLASH.ld -Wl,--gc-sections
    -Wl,-Map=${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.map -Wl,--print-memory-usage)
target_link_libraries(${PROJECT_NAME} PRIVATE c m)
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O ihex $<TARGET_FILE:${PROJECT_NAME}> ${PROJECT_NAME}.hex
    COMMAND ${CMAKE_OBJCOPY} -O binary $<TARGET_FILE:${PROJECT_NAME}> ${PROJECT_NAME}.bin
    COMMAND ${CMAKE_SIZE} $<TARGET_FILE:${PROJECT_NAME}>)
